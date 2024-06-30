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


#include <brain/robotstatemachine.hpp>

namespace brain{

    /**
     * @brief CRobotStateMachine Class constructor
     * 
     * @param f_period              period for controller execution in seconds
     * @param f_serialPort          reference to serial communication object
     * @param f_steeringControl     reference to steering motor control interface
     * @param f_speedingControl     reference to brushless motor control interface
     */
    CRobotStateMachine::CRobotStateMachine(
            uint32_t                      f_period,
            UnbufferedSerial&             f_serialPort,
            drivers::ISteeringCommand&    f_steeringControl,
            drivers::ISpeedingCommand&    f_speedingControl
        ) 
        : utils::CTask(f_period)
        , m_serialPort(f_serialPort)
        , m_steeringControl(f_steeringControl)
        , m_speedingControl(f_speedingControl)
    {
    }

    /** @brief  CRobotStateMachine class destructor
     */
    CRobotStateMachine::~CRobotStateMachine()
    {
    };

    /** \brief  _Run method contains the main application logic, where it controls the lower lever drivers (dc motor and steering) based the given command and state.
     * It has three main states: 
     *  - 1 - move state -> control the motor rotation speed by giving a speed reference, which is then converted to PWM
     *  - 2 - steering state -> trigger the steering of the motor
     *  - 3 - Brake state -> make the motor enter into a brake state.          
     */
    void CRobotStateMachine::_run()
    {   
        switch(m_state)
        {
            // speed state - control the dc motor rotation speed and the steering angle. 
            case 1:
                break;

            // Steering state
            case 2:
                break;

            // Brake state
            case 3:
                break;
        }
    }

    /** \brief  Serial callback method for speed command
     *
     * Serial callback method setting controller to value received for dc motor control values. 
     * In the case of pid activated, the dc motor control values has to be express in meter per second, otherwise represent the duty cycle of PWM signal in percent. 
     * The steering angle has to express in degree, where the positive values marks the right direction and the negative values noticed the left turning direction.
     *
     * @param a                   string to read data 
     * @param b                   string to write data 
     * 
     */
    void CRobotStateMachine::serialCallbackSPEEDcommand(char const * a, char * b)
    {
        float l_speed;
        uint32_t l_res = sscanf(a,"%f",&l_speed);
        if (1 == l_res)
        {
            if( !m_speedingControl.inRange(l_speed)){ // Check the received reference speed is within range
                sprintf(b,"The reference speed command is too high");
                return;
            }

            m_state = 1;
            m_speedingControl.setSpeed(l_speed); // Set the reference speed
            float c_speed = m_speedingControl.conversion(l_speed);
            sprintf(b,"ack");    
            sprintf(b, "Current pwm: %f", c_speed);




        }
        else
        {
            sprintf(b,"sintax error");
        }
    }

    /** \brief  Serial callback method for steering command
     *
     * Serial callback method setting controller to value received for steering angle.
     * The steering angle has to express in degree, where the positive values marks the right direction and the negative values noticed the left turning direction.
     *
     * @param a                   string to read data 
     * @param b                   string to write data 
     * 
     */
    void CRobotStateMachine::serialCallbackSTEERcommand(char const * a, char * b)
    {
        float l_angle;
        uint32_t l_res = sscanf(a,"%f",&l_angle);
        if (1 == l_res)
        {
            if( !m_steeringControl.inRange(l_angle)){ // Check the received steering angle
                sprintf(b,"The steering angle command is too high");
                return;
            }

            m_state = 2;
            m_steeringControl.setAngle(l_angle); // control the steering angle 
            sprintf(b,"ack");
            // sprintf(b, "%f", l_angle);
        }
        else
        {
            sprintf(b,"sintax error");
        }
    }

    /** \brief  Serial callback actions for brake command
     *
     * This method aims to change the state of controller to brake and sets the steering angle to the received value. 
     *
     * @param a                   string to read data 
     * @param b                   string to write data
     * 
     */
    void CRobotStateMachine::serialCallbackBRAKEcommand(char const * a, char * b)
    {
        float l_angle;
        uint32_t l_res = sscanf(a,"%f",&l_angle);
        if(1 == l_res)
        {
            if( !m_steeringControl.inRange(l_angle)){
                sprintf(b,"The steering angle command is too high");
                return;
            }
            
            
            m_state = 3;
            m_steeringControl.setAngle(l_angle); // control the steering angle 
            m_speedingControl.setBrake();
            sprintf(b,"ack");           
        }
        else
        {
            sprintf(b,"sintax error");
        }
    }

}; // namespace brain