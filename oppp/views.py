from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Item, FaceProfile
import face_recognition
import numpy as np
import cv2
from django.http import JsonResponse

# 📷 Capture Face Using Webcam
def capture_face():
    """Displays live camera feed and captures face when user presses 'SPACE'."""
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Unable to access the camera.")
            break

        # Show the video feed to the user
        cv2.imshow("Adjust Position - Press SPACE to Capture", frame)

        # Wait for user to press SPACE to capture the image
        key = cv2.waitKey(1)
        if key == ord(' '):  # Space key
            face_encodings = face_recognition.face_encodings(frame)
            if face_encodings:
                video_capture.release()
                cv2.destroyAllWindows()
                return np.array(face_encodings[0], dtype=np.float64).tobytes()

            print("No face detected, try again.")

        elif key == ord('q'):  # Quit camera feed
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return None


# 🔑 Signup View (Improved Face Handling)
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            print("Opening camera for face capture...")
            face_encoding = capture_face()  # Captures face when user presses SPACE

            if not face_encoding:
                return JsonResponse({"error": "Face not detected. Adjust position and try again."}, status=400)

            # Store face encoding in database
            FaceProfile.objects.create(user=user, face_encoding=face_encoding)

            login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


# 🏠 Home View
def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})


# 🔒 Login View (Uses Live Camera for Face Authentication)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            # Capture user's face for authentication
            face_encoding = capture_face()
            if not face_encoding:
                return JsonResponse({"error": "No face detected. Please try again."}, status=400)

            # Retrieve stored face data for this user
            stored_profile = FaceProfile.objects.filter(user=user).first()
            if not stored_profile:
                return JsonResponse({"error": "No face data found for this user."}, status=400)

            stored_encoding = np.frombuffer(stored_profile.face_encoding, dtype=np.float64)
            match = face_recognition.compare_faces([stored_encoding], np.frombuffer(face_encoding, dtype=np.float64))[0]

            if match:
                login(request, user)
                return redirect('home')
            else:
                return JsonResponse({"error": "Face does not match! Login denied."}, status=401)

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# 🚪 Logout View
def logout_view(request):
    logout(request)
    return redirect('home')