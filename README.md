<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />

<p align="center">


  <h3 align="center">Sach Ka Saamna</h3>

  <p align="center">
    An awesome website to detect image tampering. Made with Love by the team fast for  Vihaan 4.0
    <br />
    <a href="https://github.com/killer4639/sach-ka-saamna-vihaan"><strong>Explore the docs »</strong></a>
    <br />
    ·
    <a href="https://github.com/killer4639/sach-ka-saamna-vihaan/issues">Report Bug</a>
    ·
    <a href="https://github.com/killer4639/sach-ka-saamna-vihaan/issues">Request Feature</a>
  </p>
</p>

  
<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#issues">Issues</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Editing a real-world photo through computer software or mobile applications is one of the easiest things one can do today before sharing the doctored image on one’s social networking sites. Although most people do it for fun, it is suspectable if one concealed an object or changed someone’s face within the image. Before questioning the intention behind the editing operations, we need to first identify how and which part of the image has been manipulated. It therefore demands automatic tools for identifying the intrinsic difference between authentic images and tampered images. [A great survey on this topic](https://www.sciencedirect.com/science/article/abs/pii/S104732031830350X)

To address the issue we try to solve the problem in 2 phases :

1. Detecting whether image has been tampered with or not.
2. Finding the exact tampered region of an image through various deep learning techniques.
3. Making a real-world usable product out of the model we generated that can be used by anyone.
4. This product has scope of being extended to a fully functional product which can be used by security agencies.

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

- [Python](https://www.python.org)
- [JQuery](https://jquery.com)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Tensorflow](https://www.tensorflow.org/)
- [OpenCV](https://www.opencv.org/)
- [Keras](https://www.keras.io)
- [NumPy](https://www.numpy.org/)
- [Matplotlib](https://www.matplotlib.org/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- [Python 3.7+](https://www.python.org/downloads/)
- Make a bucket on Amazon AWS S3 and download the keys. Make sure your bucket is public.
- Create an .env file with the following keys. (Team Vihaan- Please contact anyone from below contacts for S3 keys if there is a difficulty in using S3 or if you want to test with S3 without making an AWS account) 

  ```
  export S3_BUCKET=<Bucket Name>
  export S3_SECRET_ACCESS_KEY=<AWSSecretKey>
  export S3_KEY=<AWSAccessKeyId>
  export S3_REGION=<AWS Region>
  export DATABASE_URL= <if you are using any postgresql hosted database then db url>
  ```
  
 - Make folder structure of the folder 'models' in the following way after downloading the models from and [here](https://drive.google.com/drive/folders/146X2Z_ubUO8W_0JLEx8Jrvw8937MUr2q?usp=sharing) and arrange them respectively
 
```
models
|--- segmentation
|    ├── model.json
|    └── model_for_json.h5
|     
|--- model.json
|--- model_weights.h5
```

### Installation

1. Clone the repo
   ```
   $ git clone https://github.com/killer4639/sach-ka-saamna-vihaan.git
   $ cd verisimilitudo-codecamp
   ```
2. Activating virtual environment (optional)
   ```
   $ python -m venv venv
   $ venv\Scripts\activate
   ```
3. Install requirements
   ```
   $ pip install -r requirements.txt
   ```
4. Run Application

   ```
   $ python app.py
   ```

5. Issues while running

   ```
    If you encounter an issue on your terminal like this
    KeyError: 'DATABASE_URL'
    It is because you don't have any  postresql online hosted database. Use the local one as given. Or uncomment it from scripts/tabledef.py

    Images get stored in the assets folder
   ```

<!-- USAGE EXAMPLES -->

## Usage

This video explains how to use the version 2.0 which classifies an image if its fake or real and shows the tampered regions. Let's watch this

We are developing a slack/ telegram bot for using it

The white region represents- Tampering





Notebook walkthrough to understand algorithm







<!-- ROADMAP -->

## Roadmap

- Building the model. We have used tensorflow and keras to train and build the model.
- Creating the web app for actual usability of our idea and not just a script to watch
- Finally deploying it to heroku which took us more than a day because of our huge slug size and complexity
- We are still not able to deploy the application which shows the location in the image with tampering because of our increased slug size and the limits of Heroku but we have our Version 1.0 ready :D

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
<a href="https://github.com/killer4639/sach-ka-saamna-vihaan/blob/master/CONTRIBUTING.md">Read our contributing guidelines</a>

<!-- ISSUES -->

## Issues

- After resetting the password if we logout, then it doesn't login with the new credentials. This needs to be looked upon.
- The compute timing on local machine is slow and hence we can use any cloud service for our model computations which will return a JSON object with image and result. This will also help us to deploy on Heroku with less slug size.
- Better error handling and unit testing. Eg. error is encountered if without uploading any image, we click predict.
- Email verification
- Making it mobile responsive and UI additions.

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

- [Anikash Chakraborty](https://www.linkedin.com/in/anikash-chakraborty/) (mailto: akh.chakraborty11@gmail.com)
- [Shiva Gupta](https://www.linkedin.com/in/shiva-gupta-1843b6170/) (mailto: shivagupta4639@gmail.com)
- [Divyansh Goel](https://www.linkedin.com/in/divyansh-goel-a0a433166/) (mailto: divyanshgoel1999@gmail.com)
- Project Link: [https://github.com/killer4639/sach-ka-saamna-vihaan](https://github.com/killer4639/sach-ka-saamna-vihaan)

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

- [Img Shields](https://shields.io)
- [CASIA 2.0 Dataset](https://github.com/namtpham/casia2groundtruth)
- [MIT License](https://spdx.org/licenses/MIT.html)
- [Anfederico](https://github.com/anfederico/flaskex)
- [Heroku](https://www.heroku.com)
- [Font Awesome](https://fontawesome.com)
- [OBS Studio](https://obsproject.com)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/killer4639/sach-ka-saamna-vihaan.svg?style=for-the-badge
[contributors-url]: https://github.com/killer4639/sach-ka-saamna-vihaan/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/killer4639/sach-ka-saamna-vihaan.svg?style=for-the-badge
[forks-url]: https://github.com/killer4639/sach-ka-saamna-vihaan/network/members
[stars-shield]: https://img.shields.io/github/stars/killer4639/sach-ka-saamna-vihaan.svg?style=for-the-badge
[stars-url]: https://github.com/killer4639/sach-ka-saamna-vihaan/stargazers
[issues-shield]: https://img.shields.io/github/issues/killer4639/sach-ka-saamna-vihaan.svg?style=for-the-badge
[issues-url]: https://github.com/killer4639/sach-ka-saamna-vihaan/issues
[license-shield]: https://img.shields.io/github/license/killer4639/sach-ka-saamna-vihaan.svg?style=for-the-badge
[license-url]: https://github.com/killer4639/sach-ka-saamna-vihaan/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/anikash-chakraborty/

