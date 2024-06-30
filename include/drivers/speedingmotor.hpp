/**
 * Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC organizers
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:

 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions and the following disclaimer.

 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.

 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.

 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
*/

/* Include guard */
#ifndef SPEEDINGMOTOR_HPP
#define SPEEDINGMOTOR_HPP

/* The mbed library */
#include <mbed.h>

namespace drivers
{
    /**
     * @brief Interface to control the brushless motor.
     * 
     */
    class ISpeedingCommand
    {
        public:
            virtual void setSpeed(float f_speed) = 0 ;
            virtual bool inRange(float f_speed) = 0 ;
            virtual void setBrake() = 0 ;
            virtual float conversion(float f_speed) = 0; 
    };

    /**  
     * @brief Speeding motor driver
     * 
     * It is used to control the Brushless motor (more precisely the ESC), which is connected to driving shaft. The reference speed can be accessed through 'setSpeed' method. 
     * 
     */
    class CSpeedingMotor: public ISpeedingCommand
    {
        public:
            /* Constructor */
            CSpeedingMotor();
            CSpeedingMotor(
                PinName     f_pwm_pin,
                float       f_inf_limit,
                float       f_sup_limit
            );
            /* Destructor */
            ~CSpeedingMotor();
            /* Set speed */
            void setSpeed(float f_speed); 
            /* Check speed is in range */
            bool inRange(float f_speed);
            /* Set brake */
            void setBrake(); 
            /* Check speed */
            float conversion(float f_speed); //angle to duty cycle

        private:
            /** @brief PWM output pin */
            PwmOut m_pwm_pin;
            /** @brief 0 default */
            // float zero_default = -0.0974343; // min
            float zero_default = 0.10250402; 

            /** @brief 0 default */
            int8_t ms_period = 15.9;
            // float ms_period = 14.85;
            /** @brief step_value */
            float step_value = 0.00063;
            /** @brief Inferior limit */
            const float m_inf_limit;
            /** @brief Superior limit */
            const float m_sup_limit;

            /* interpolate the step value based on the speed value */
            float interpolate(float speed, const float speedValuesP[], const float speedValuesN[], const float stepValues[], int size);

            // Predefined values for steering reference and interpolation
            const float speedValuesP[25] = {4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 26.0, 30.0, 35.0, 40.0, 45.0, 50.0};
            const float speedValuesN[25] = {-4.0, -5.0, -6.0, -7.0, -8.0, -9.0, -10.0, -11.0, -12.0, -13.0, -14.0, -15.0, -16.0, -17.0, -18.0, -19.0, -20.0, -21.0, -22.0, -26.0, -30.0, -35.0, -40.0, -45.0, -50.0};
            // const float stepValues[25] = {0.00107, 0.00088, 0.00076, 0.00067, 0.0006, 0.00055, 0.00051, 0.00047, 0.00043, 0.00041, 0.00039, 0.00037, 0.00035, 0.00034, 0.00033, 0.00032,
            //                               0.0003, 0.00029, 0.00028, 0.00025, 0.00024, 0.00021, 0.00019, 0.00018, 0.00017};
            // const float stepValues[25] = {0, 0.00326118, 0.00281647, 0.00248294, 0.00222353, 0.00203824, 0.00189, 0.00174176, 0.00159353, 0.00151941, 0.00144529, 0.00137118, 0.00129706,
                                            // 0.00126, 0.00122294, 0.00118588, 0.00111176, 0.00107471, 0.00103765, 0.000926471, 0.000889412, 0.000778235, 0.000704118, 0.000667059, 0.00063};
            const float stepValues[25] = {
                0,
                0.000465882,
                0.000402353,
                0.000354706,
                0.000317647,
                0.000291176,
                0.00027,
                0.000248824,
                0.000227647,
                0.000217059,
                0.000206471,
                0.000195882,
                0.000185294,
                0.00018,
                0.000174706,
                0.000169412,
                0.000158824,
                0.000153529,
                0.000148235,
                0.000132353,
                0.000127059,
                0.000111176,
                0.000100588,
                9.52941e-05,
                9e-05,
            };
            /* convert speed value to duty cycle for pwm signal */
            static float pwm_value;

            
    }; // class CSpeedingMotor
}; // namespace drivers

#endif// SPEEDINGMOTOR_HPP