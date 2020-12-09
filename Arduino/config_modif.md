The config.h file was modified as follow:  
// #define HOMING_CYCLE_0 ((1<<X_AXIS)|(1<<Y_AXIS))  // NOT COMPATIBLE WITH COREXY: Homes both X-Y in one cycle. 

#define HOMING_CYCLE_0 (1<<X_AXIS)  // COREXY COMPATIBLE: First home X  
#define HOMING_CYCLE_1 (1<<Y_AXIS)  // COREXY COMPATIBLE: Then home Y  

And :  
#define HOMING_FORCE_SET_ORIGIN // Uncomment to enable.

