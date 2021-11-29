import streamlit as st

from PIL import Image
import numpy as np
import cv2

# ------------------------------
from PIL import Image
from pyzbar.pyzbar import decode
# ------------------------------

# DEMO_IMAGE = 'sample_file.png'

st.set_page_config(page_icon='icon.png',page_title='QR Code Decoder',layout='centered')
# title of the web-app
st.title('QR Code Decoder')
st.markdown('''Decode ***almost*** any QR code ''')


@st.cache
def show_qr_detection(img, pts):

    pts = np.int32(pts).reshape(-1, 2)

    for j in range(pts.shape[0]):

        cv2.line(img, tuple(pts[j]), tuple(
            pts[(j + 1) % pts.shape[0]]), (255, 0, 0), 5)

    for j in range(pts.shape[0]):
        cv2.circle(img, tuple(pts[j]), 10, (255, 0, 255), -1)


@st.cache
def qr_code_dec(image):

    decoder = cv2.QRCodeDetector()

    data, vertices, rectified_qr_code = decoder.detectAndDecode(image)

    if len(data) > 0:
        print("Decoded Data: '{}'".format(data))

    # Show the detection in the image:
        show_qr_detection(image, vertices)

        rectified_image = np.uint8(rectified_qr_code)

        decoded_data = data  # 'Decoded data: '+

        rectified_image = cv2.putText(rectified_image, decoded_data, (50, 350), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=2,
                                      color=(250, 225, 100), thickness=3, lineType=cv2.LINE_AA)

    return decoded_data

# uploading the imges
img_file_buffer = st.file_uploader(
    "Upload QR code to Decode", type=["jpg", "jpeg", 'png'])

@st.cache
def yet_another_decoder(image):

    data = decode(Image.open(image))
    return (str(data[0].data).replace('b', '').replace("'", ""))


if img_file_buffer is not None:
    image = np.array(Image.open(img_file_buffer))

# else:
#     demo_image = DEMO_IMAGE
#     image = np.array(Image.open(demo_image))

    st.subheader('Uploaded Image : ')

    # display the image
    st.image(
        image, caption=f"", use_column_width=True
    )


# Another decoder section

    try:
        decoded_data = qr_code_dec(image)
        st.subheader('Decoded data : ')
        st.info(decoded_data)
        # st.text_area(qr_code_dec(image))
    except UnboundLocalError:

        try:
            st.subheader('Decoded data : ')
            st.info(yet_another_decoder(img_file_buffer))
            # yet_another_decoder(image)
        except IndexError:

            st.error('''QR code invalid... enter a valid QR code''')



st.markdown("<h5 style='text-align: center; color: white;'>🙂 Developed by  <a href='https://www.rohan.contact' target='_blank'>Rohan Madhale</a> 🙂 </h5>", unsafe_allow_html=True)
