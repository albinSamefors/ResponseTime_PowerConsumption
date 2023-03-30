/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
SPI_HandleTypeDef hspi1;

TIM_HandleTypeDef htim2;

PCD_HandleTypeDef hpcd_USB_FS;

/* USER CODE BEGIN PV */
struct TimeCapture{
	uint32_t startTime;
	uint32_t endTime;
};
uint16_t captures = 0;
struct TimeCapture timeBuff;
struct TimeCapture lastBuff;
_Bool timeBuffReady = false;
_Bool run_test = false;
_Bool finished = false;

//DATA FETCHED FROM SPI
_Bool RecievedTransmitHeader = false;
uint16_t sleep_time;
uint16_t max_amount_of_runs;
uint16_t test_mode = 2;
_Bool test_input_set = false;
//CREATE AFTER DATA HAS BEEN RECIEVED
//struct TimeCapture data_us[MAX_AMOUNT_OF_RUNS];
uint32_t timer_val;
uint32_t debug_value = 1000;
//SPI REGISTER DATA
typedef enum Header {
	SLEEP_TIME = 1,
	RUN_AMOUNT = 2,
	TEST_MODE = 3
} Header;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
void PeriphCommonClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USB_PCD_Init(void);
static void MX_TIM2_Init(void);
static void MX_SPI1_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
_Bool recieve16Bit(uint16_t *read_to){

	if(HAL_SPI_Receive(&hspi1, (uint8_t*)read_to, 2, 10) == HAL_OK) {
		return true;
	}

	return false;
}

_Bool send16Bit(uint16_t *send){
	if(HAL_SPI_Transmit(&hspi1, (uint8_t*)send, 2,10) == HAL_OK){
		return true;

	}
	return false;
}

void getStartInput(){
	uint8_t header;
		  HAL_StatusTypeDef receive_status = HAL_SPI_Receive(&hspi1, &header, 1, 10);
		  if(receive_status == HAL_OK) {
			  switch((Header)header) {
			  	  case SLEEP_TIME:
			  		  if(!recieve16Bit(&sleep_time)) {
			  			  printf("ERROR COULD NOT RECIEVE SLEEP TIME");
			  		  	  }
					  break;
				  case RUN_AMOUNT:
					  if(!recieve16Bit(&max_amount_of_runs)){
						  printf("ERROR COULD NOT RECIEVE AMOUNT OF RUNS");
					  }

					  break;
				  case TEST_MODE:
					  if(!recieve16Bit(&test_mode)){
						  printf("TEST MODE COULD NOT BE RECIEVED");
					  }
					  break;
				  }
		  }
		  if(test_mode != 2){
			  test_input_set = true;
		  }
}
void sendTestData(uint32_t *times){
	uint16_t index = 0;
	HAL_GPIO_WritePin(TransmitReady_GPIO_Port, TransmitReady_Pin, GPIO_PIN_SET);
	while(index < max_amount_of_runs){
		uint8_t header;
		uint32_t *ptr = &times[index];
		uint16_t value = *((uint16_t*)ptr);
		HAL_StatusTypeDef recieve_status = HAL_SPI_Receive(&hspi1, &header, 1, 10);
		if(recieve_status == HAL_OK){
			if(header == 4){
				if(!send16Bit(&value)){
					printf("COULD NOT SEND DATA");
				}
				index++;
			}
			else{
				printf("STUB");
			}
		}
	}
	HAL_GPIO_WritePin(TransmitReady_GPIO_Port, TransmitReady_Pin, GPIO_PIN_RESET);
}

void sendData(uint32_t *data){

		for(int i = 0; i < max_amount_of_runs; i++){
			uint32_t *ptr = &data[i];
			uint16_t value = *((uint16_t*)ptr);
			send16Bit(&value);

	}
}

void calculateTestTimes(struct TimeCapture *data, uint32_t *times){
	for(int i = 0; i < max_amount_of_runs; i++){
		struct TimeCapture *time_ptr = &data[i];
		uint32_t *ptr = &times[i];
		uint32_t start_time = time_ptr->startTime;
		uint32_t end_time = time_ptr->endTime;
		uint32_t fullTime;
		if(end_time >= start_time){
			fullTime = end_time - start_time;
		}
		else{
			fullTime = (TIM2->ARR - start_time) + end_time;
		}
		uint32_t wake_up_time = fullTime - (sleep_time * 1000);
		debug_value = fullTime;
		*ptr = wake_up_time;
	}
}

void sendInterrupt(){
	HAL_GPIO_WritePin(Interrupter_GPIO_Port, Interrupter_Pin, GPIO_PIN_SET);
	HAL_GPIO_WritePin(Interrupter_GPIO_Port, Interrupter_Pin, GPIO_PIN_RESET);
}

void testUsingInterrupts(struct TimeCapture *times){
	int i = 0;
	while(run_test){
		struct TimeCapture *time_ptr = &times[i];
		HAL_Delay(sleep_time);
		sendInterrupt();
		while(!timeBuffReady);
		*time_ptr = timeBuff;
		i++;
		timeBuff.startTime = 0;
		timeBuff.endTime = 0;
		timeBuffReady = false;
		if(captures == max_amount_of_runs * 2){
			run_test = false;
		}
	}
}

void testUsingIntervals(struct TimeCapture *times){
	int i = 0;
	while(run_test){
		struct TimeCapture *time_ptr = &times[i];
		while(!timeBuffReady);
		*time_ptr = timeBuff;
		i++;
		lastBuff = timeBuff;
		timeBuff.startTime = 0;
		timeBuff.endTime = 0;
		timeBuffReady = false;
		if(captures == max_amount_of_runs * 2){
			run_test = false;
		}

	}
}


/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

/* Configure the peripherals common clocks */
  PeriphCommonClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USB_PCD_Init();
  MX_TIM2_Init();
  MX_SPI1_Init();
  /* USER CODE BEGIN 2 */
  HAL_TIM_Base_Start(&htim2);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
	  if(!finished){
	  if(!test_input_set){
	 	  	  getStartInput();
	 	  }
	 	  else{
	 		  struct TimeCapture times[max_amount_of_runs];
	 		  if(test_mode == 1){
	 			  // RUN TESTS USING ITERRUPTS
	 			  run_test = true;
	 			  testUsingInterrupts(times);
	 			  uint32_t test_times[max_amount_of_runs];
	 			  calculateTestTimes(times,test_times);
	 			  sendData(test_times);
	 			  finished = true;
	 		  }
	 		  else{
	 			  run_test = true;
	 			  testUsingIntervals(times);
	 			  uint32_t test_times[max_amount_of_runs];
	 			  calculateTestTimes(times, test_times);
	 			  sendTestData(test_times);
	 			  finished = true;
	 		  }
	 	  }
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

	  }
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Macro to configure the PLL multiplication factor
  */
  __HAL_RCC_PLL_PLLM_CONFIG(RCC_PLLM_DIV1);

  /** Macro to configure the PLL clock source
  */
  __HAL_RCC_PLL_PLLSOURCE_CONFIG(RCC_PLLSOURCE_MSI);

  /** Configure LSE Drive Capability
  */
  HAL_PWR_EnableBkUpAccess();
  __HAL_RCC_LSEDRIVE_CONFIG(RCC_LSEDRIVE_LOW);

  /** Configure the main internal regulator output voltage
  */
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI|RCC_OSCILLATORTYPE_HSE
                              |RCC_OSCILLATORTYPE_LSE|RCC_OSCILLATORTYPE_MSI;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.LSEState = RCC_LSE_ON;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.MSIState = RCC_MSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.MSICalibrationValue = RCC_MSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.MSIClockRange = RCC_MSIRANGE_6;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure the SYSCLKSource, HCLK, PCLK1 and PCLK2 clocks dividers
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK4|RCC_CLOCKTYPE_HCLK2
                              |RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSE;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.AHBCLK2Divider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.AHBCLK4Divider = RCC_SYSCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Enable MSI Auto calibration
  */
  HAL_RCCEx_EnableMSIPLLMode();
}

/**
  * @brief Peripherals Common Clock Configuration
  * @retval None
  */
void PeriphCommonClock_Config(void)
{
  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};

  /** Initializes the peripherals clock
  */
  PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_SMPS;
  PeriphClkInitStruct.SmpsClockSelection = RCC_SMPSCLKSOURCE_HSI;
  PeriphClkInitStruct.SmpsDivSelection = RCC_SMPSCLKDIV_RANGE0;

  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN Smps */

  /* USER CODE END Smps */
}

/**
  * @brief SPI1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI1_Init(void)
{

  /* USER CODE BEGIN SPI1_Init 0 */

  /* USER CODE END SPI1_Init 0 */

  /* USER CODE BEGIN SPI1_Init 1 */

  /* USER CODE END SPI1_Init 1 */
  /* SPI1 parameter configuration*/
  hspi1.Instance = SPI1;
  hspi1.Init.Mode = SPI_MODE_SLAVE;
  hspi1.Init.Direction = SPI_DIRECTION_2LINES;
  hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi1.Init.NSS = SPI_NSS_HARD_INPUT;
  hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi1.Init.CRCPolynomial = 7;
  hspi1.Init.CRCLength = SPI_CRC_LENGTH_DATASIZE;
  hspi1.Init.NSSPMode = SPI_NSS_PULSE_DISABLE;
  if (HAL_SPI_Init(&hspi1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI1_Init 2 */

  /* USER CODE END SPI1_Init 2 */

}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM2_Init(void)
{

  /* USER CODE BEGIN TIM2_Init 0 */

  /* USER CODE END TIM2_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM2_Init 1 */

  /* USER CODE END TIM2_Init 1 */
  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 32-1;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 4294967295;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim2, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM2_Init 2 */

  /* USER CODE END TIM2_Init 2 */

}

/**
  * @brief USB Initialization Function
  * @param None
  * @retval None
  */
static void MX_USB_PCD_Init(void)
{

  /* USER CODE BEGIN USB_Init 0 */

  /* USER CODE END USB_Init 0 */

  /* USER CODE BEGIN USB_Init 1 */

  /* USER CODE END USB_Init 1 */
  hpcd_USB_FS.Instance = USB;
  hpcd_USB_FS.Init.dev_endpoints = 8;
  hpcd_USB_FS.Init.speed = PCD_SPEED_FULL;
  hpcd_USB_FS.Init.phy_itface = PCD_PHY_EMBEDDED;
  hpcd_USB_FS.Init.Sof_enable = DISABLE;
  hpcd_USB_FS.Init.low_power_enable = DISABLE;
  hpcd_USB_FS.Init.lpm_enable = DISABLE;
  hpcd_USB_FS.Init.battery_charging_enable = DISABLE;
  if (HAL_PCD_Init(&hpcd_USB_FS) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USB_Init 2 */

  /* USER CODE END USB_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(Interrupter_GPIO_Port, Interrupter_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, LD2_Pin|LD3_Pin|TransmitReady_Pin|LD1_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : TestStartInput_Pin */
  GPIO_InitStruct.Pin = TestStartInput_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(TestStartInput_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : Interrupter_Pin */
  GPIO_InitStruct.Pin = Interrupter_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(Interrupter_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : TestStopInput_Pin */
  GPIO_InitStruct.Pin = TestStopInput_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  HAL_GPIO_Init(TestStopInput_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : LD2_Pin LD3_Pin TransmitReady_Pin LD1_Pin */
  GPIO_InitStruct.Pin = LD2_Pin|LD3_Pin|TransmitReady_Pin|LD1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : B2_Pin B3_Pin */
  GPIO_InitStruct.Pin = B2_Pin|B3_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI0_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI0_IRQn);

  HAL_NVIC_SetPriority(EXTI2_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI2_IRQn);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin){

	if(GPIO_Pin == TestStartInput_Pin){
		timeBuff.startTime = __HAL_TIM_GET_COUNTER(&htim2);

		if(captures < max_amount_of_runs*2){
			captures++;
		}

	}

	if(GPIO_Pin == TestStopInput_Pin){
		timeBuff.endTime = __HAL_TIM_GET_COUNTER(&htim2);
		if(timeBuff.endTime != 0){
		timeBuffReady = true;
		}
		if(captures < max_amount_of_runs * 2){
			captures++;
		}
	}

}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
