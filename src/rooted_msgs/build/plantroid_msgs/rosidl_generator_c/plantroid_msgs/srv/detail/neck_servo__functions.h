// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from plantroid_msgs:srv/NeckServo.idl
// generated code does not contain a copyright notice

#ifndef PLANTROID_MSGS__SRV__DETAIL__NECK_SERVO__FUNCTIONS_H_
#define PLANTROID_MSGS__SRV__DETAIL__NECK_SERVO__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "plantroid_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "plantroid_msgs/srv/detail/neck_servo__struct.h"

/// Initialize srv/NeckServo message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * plantroid_msgs__srv__NeckServo_Request
 * )) before or use
 * plantroid_msgs__srv__NeckServo_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
bool
plantroid_msgs__srv__NeckServo_Request__init(plantroid_msgs__srv__NeckServo_Request * msg);

/// Finalize srv/NeckServo message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
void
plantroid_msgs__srv__NeckServo_Request__fini(plantroid_msgs__srv__NeckServo_Request * msg);

/// Create srv/NeckServo message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * plantroid_msgs__srv__NeckServo_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
plantroid_msgs__srv__NeckServo_Request *
plantroid_msgs__srv__NeckServo_Request__create();

/// Destroy srv/NeckServo message.
/**
 * It calls
 * plantroid_msgs__srv__NeckServo_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
void
plantroid_msgs__srv__NeckServo_Request__destroy(plantroid_msgs__srv__NeckServo_Request * msg);


/// Initialize array of srv/NeckServo messages.
/**
 * It allocates the memory for the number of elements and calls
 * plantroid_msgs__srv__NeckServo_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
bool
plantroid_msgs__srv__NeckServo_Request__Sequence__init(plantroid_msgs__srv__NeckServo_Request__Sequence * array, size_t size);

/// Finalize array of srv/NeckServo messages.
/**
 * It calls
 * plantroid_msgs__srv__NeckServo_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
void
plantroid_msgs__srv__NeckServo_Request__Sequence__fini(plantroid_msgs__srv__NeckServo_Request__Sequence * array);

/// Create array of srv/NeckServo messages.
/**
 * It allocates the memory for the array and calls
 * plantroid_msgs__srv__NeckServo_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
plantroid_msgs__srv__NeckServo_Request__Sequence *
plantroid_msgs__srv__NeckServo_Request__Sequence__create(size_t size);

/// Destroy array of srv/NeckServo messages.
/**
 * It calls
 * plantroid_msgs__srv__NeckServo_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
void
plantroid_msgs__srv__NeckServo_Request__Sequence__destroy(plantroid_msgs__srv__NeckServo_Request__Sequence * array);

/// Initialize srv/NeckServo message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * plantroid_msgs__srv__NeckServo_Response
 * )) before or use
 * plantroid_msgs__srv__NeckServo_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
bool
plantroid_msgs__srv__NeckServo_Response__init(plantroid_msgs__srv__NeckServo_Response * msg);

/// Finalize srv/NeckServo message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
void
plantroid_msgs__srv__NeckServo_Response__fini(plantroid_msgs__srv__NeckServo_Response * msg);

/// Create srv/NeckServo message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * plantroid_msgs__srv__NeckServo_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
plantroid_msgs__srv__NeckServo_Response *
plantroid_msgs__srv__NeckServo_Response__create();

/// Destroy srv/NeckServo message.
/**
 * It calls
 * plantroid_msgs__srv__NeckServo_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
void
plantroid_msgs__srv__NeckServo_Response__destroy(plantroid_msgs__srv__NeckServo_Response * msg);


/// Initialize array of srv/NeckServo messages.
/**
 * It allocates the memory for the number of elements and calls
 * plantroid_msgs__srv__NeckServo_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
bool
plantroid_msgs__srv__NeckServo_Response__Sequence__init(plantroid_msgs__srv__NeckServo_Response__Sequence * array, size_t size);

/// Finalize array of srv/NeckServo messages.
/**
 * It calls
 * plantroid_msgs__srv__NeckServo_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
void
plantroid_msgs__srv__NeckServo_Response__Sequence__fini(plantroid_msgs__srv__NeckServo_Response__Sequence * array);

/// Create array of srv/NeckServo messages.
/**
 * It allocates the memory for the array and calls
 * plantroid_msgs__srv__NeckServo_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
plantroid_msgs__srv__NeckServo_Response__Sequence *
plantroid_msgs__srv__NeckServo_Response__Sequence__create(size_t size);

/// Destroy array of srv/NeckServo messages.
/**
 * It calls
 * plantroid_msgs__srv__NeckServo_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_plantroid_msgs
void
plantroid_msgs__srv__NeckServo_Response__Sequence__destroy(plantroid_msgs__srv__NeckServo_Response__Sequence * array);

#ifdef __cplusplus
}
#endif

#endif  // PLANTROID_MSGS__SRV__DETAIL__NECK_SERVO__FUNCTIONS_H_
