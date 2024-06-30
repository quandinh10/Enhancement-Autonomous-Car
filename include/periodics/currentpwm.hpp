// #ifndef CURRENTPWM_HPP
// #define CURRENTPWM_HPP

// // TODO: Add your code here
// /* The mbed library */
// #include <mbed.h>
// /* Header file for the task manager library, which  applies periodically the fun function of it's children*/
// #include <utils/task.hpp>
// #include <drivers/speedingmotor.hpp>
// namespace periodics
// {
//    /**
//     * @brief Class currentpwm
//     * Use to return pwn of motor
//     *
//     */
//     class CCurrentpwm : public utils::CTask
//     {
//         public:
//             /* Construnctor */
//             CCurrentpwm(
//                 uint32_t        f_period, 
//                 PinName         pin_name,
//                 PwmOut          f_pwm_pin
//             );
//             /* Destructor */
//             ~CCurrentpwm();
//         private:
//             PinName     pin_name;
//             PwmOut f_pwm_pin;
//             /* private variables & method member */
//     }; // class CCurrentpwm
// }; // namespace periodics

// #endif // CURRENTPWM_HPP
