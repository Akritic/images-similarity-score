import cv2


def find_similarity(image1, image2):
  '''
  Using SIFT features to measure image similarity
  @args:
    {str} image1: the path to an image file
    {str} image2: the path to an image file
  '''
  
  # initialize the sift feature detector
  orb = cv2.ORB_create()

  # get the images
  image_one = cv2.imread(image1)
  image_two = cv2.imread(image2)

  # find the keypoints and descriptors with SIFT
  kp_image1, desc_image1 = orb.detectAndCompute(image_one, None)
  kp_image2, desc_image2 = orb.detectAndCompute(image_two, None)

  # initialize the bruteforce matcher
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

  # match.distance is a float between {0:100} - lower means more similar
  matches = bf.match(desc_image1, desc_image2)
  similar_regions = [i for i in matches if i.distance < 70]
  if len(matches) == 0:
    return 0

  result = str((len(matches) - len(similar_regions)) / len(matches))

  return result if result != '0.0' else '0'
