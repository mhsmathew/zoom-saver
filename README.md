

## Inspiration

Since the dawn of Zoom university and using our computer's webcam to engage in our classes, many people have been struck by the unfortunate situation of being embarrassed by an inopportune moment where they forgot their camera was on during class. Although (thankfully) this has not happened to me, just the anxiety of such an event has made me anxious whenever I connect to a class. This paired with the looming threat of hackers looking through our camera, I created this tool to mitigate all those risks.

## What it does

Imagine a student gets distracted during class (it happens) and they navigate away from Zoom for an extended period of time. Now what happens next is our app detects this event and tells the automated webcam cover to close in order to prevent any risk of an embarrassing event while distracted. Not to mention many students already have privacy covers for their cameras that they control manually, this just does that with some added features.


There are 3 modes that our webcam cover can run in through our GUI:

 - Manual Mode
	 - Users can close and open the webcame
 - Automated Mode
	 - Our app tracks when the user leaves Zoom for an extended period of time and closes the camera
	 - Whenever this event is triggered, an SMS and Mac notifications are sent in order to inform the user if they are away from their computer
 - Scheduler Mode
	 - Many users would rather only have their camera being open when they need to during class in case of a threat of being hacked, so this mode pulls course information from the student's schedule in order to only have their camera visible when class is in session
	 - When the user has class the webcam is shown, and when there is no class, it is hidden by default for privacy reasons

## How we built it

### The Hardware
Firstly, this app uses an Arduino and Servo motor in order to run the webcam cover. Using some handy C code (and duct tape for mounting), I was able to programmably control the webcam cover.

### The Web GUI
I found this very intuitive Python library that allows for easy GUI creation called [Rumps](https://github.com/jaredks/rumps) which controls the front end. The menu is very simple and it even runs in the top Menu Bar in order to be as minimally intrusive as possible.

### The Backend

Privacy was a big motivation for this project, and it mainly runs by monitoring the current app that the user is on. Then doing some calculations, we can determine whether or not to close the camera cover. Finally, after covering the webcam, we utilize [Courier's](https://www.courier.com) useful API to send a quick SMS to the user in case they were away from their computer.

## Challenges we ran into

The main hurdle for me with this project was my inexperience with using any type of hardware. I had never worked with an Arduino or servo motor before, so I had very little understanding of pins and serials. Luckily, thanks to the awesome presentations at Bitcamp, as well as Youtube, I was able to overcome this with a lot of trial and error.

## Accomplishments that we're proud of

I was very surprised to learn how useful Arduino-controlled servos can be for projects like this. I am pretty proud of creating a working webcam cover that really does satisfy the anxiety of many students like myself when having a camera on in our private homes. Also, being able to notify people have these changes can be very helpful for those of us that are rather forgetful.

## What we learned

I learned a great amount about controlling servos and hardware as well as many new frameworks and APIs. It was a great experience.

## What's next for Zoom Saver

I plan to add more features that can be more useful for students in the time of Zoom University, like detecting when you've gone away from the camera, other movement detection, and more.