# Project NightLight

This group project was created for the Electrial and Computer Engineering Design Course (ECE 180D) at UCLA.<br />
Forked from: https://github.com/180D-FW-2020/Team6

## Project Description:
Careful monitoring of your baby is a universal duty for every great parent. But for a lot of people, 
adjusting to parenthood can be challenging when juggling work, pets, family, hobbies, and much more. 
Introducing NightLight, a solution that helps parents securely monitor their infants with a low cost device that has can compete with industry standard technologies.

The NightLight Baby Monitor implements many features:
1. Motion detection with its infrared video stream that operates in all light conditions.
2. Sound classification with an audio stream capable of filtering and recording audio to determine your baby's cries.
3. Instant notifications through email of any suspicious activities from the babyside.
4. Pose recognition from an IMU that updates whenever your baby is standing upright or laying face-up or face-down.
5. Intuitive GUI with encrypted login system and array of commands including playing lullabies and downloading recordings.
5. Voice recognition for hands-free, "Siri-like" commands.

All of these are integrated into a device with real time and secure performance at a low cost. With its competitive abilities, 
the NightLight baby monitor has lots of room to excel in the stable market of infant products.

## My Contributions:
- Audio Subsystem:
  - Real-time audio transmission from the NightLight microphone to the user's GUI.
  - Noise detection.
  - Audio classification: classifies noise into five classes using Keras from Tensorflow.

- AWS EC2 Relay Server:
  - Launched EC2 instance that will run multiple programs that relays data from NightLight to GUI.
  - Audio data relay program:
    - Multithreaded program.
    - One thread listening for client connections.
    - One thread for sending audio data from NightLight to connected clients.

- AWS RDS (PostgreSQL):
  - Launched an RDS private to our EC2 server.
  - Holds user information which includes username, email, encrypted password, and notification setting.
  - Wrote a server that accepts requests via tcp from clients:
    - Create a user (checks for uniqueness).
    - Login a user.
    - Update user information and notification setting.

- AWS S3:
  - Launched an S3 bucket private to our EC2 server.
  - Holds audio recordings for audio playback in GUI.
  - Wrote a server that accepts requests via tcp from clients:
    - List all recordings.
    - Download a recording.

- Notification Subsystem:
  - Push notication via email on noise detection.
  - Requests database server for an up-to-date list of registered emails. 

## Team
Robert Renzo Rudio https://github.com/robertrenzorudio<br />
Henry Kou: https://github.com/kenryhou2<br />
Leondi Fungestu Soetojo: https://github.com/Leondi0908<br />
Denny Tsai: https://github.com/denny880320
