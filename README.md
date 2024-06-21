# Theft Detection Notifier

This program tracks the objects which comes in the frame and then send an email(with photo attachment) to the user that an object is detected. 
- I am using OpenCv libracy to capture video from the webcamera.
- To send the email I am using EmailMessage class(Python's built-in class)
- Once it detects the objects,it start saving the images and then sends an email with image attachment. And once the program ends it deletes all the images.
- I employed THREADING to ensure that the video handling, email sending, and image clearing functionalities all operate simultaneously.

  ## STEPS FOR DETECTING THE OBJECT
  - I am reading the Video frames using OpenCv library
  - Once I get my 1st frame, I am assigning it to a variable called 'first_frame'
  - Then I am converting my frame to gray frame using COLOR_BGR2GRAY algorithm, converting the image to gray frame will reduce the amount of data in matrices.
  - Then I used GaussianBlur() to blur the frame.
  - then I used absdiff() to find out the difference btw first_frame and current frame.
  - Then I am using threshold to change the object into white pixels, this will smooth the pixels.
  - Then I am adding the rectangle around the object
  - Once programs find that there is a rectangle, it will start saving all the images in the image folder.
  - Once the object leaves the video,It will take the middle frame and send it to the send_email method.
  - Because of threading video will not freeze and it will keep on tracking while in the backend send_email() will send the email.
  - Once all this is done and user ends the program,all the images from the image folder will be deleted.
