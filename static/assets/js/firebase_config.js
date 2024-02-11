const firebaseConfig = {
    apiKey: "AIzaSyDrH0S8A8u5qn7jBaVH4jHqTFCMoISOncU",
    authDomain: "instello-5ed0e.firebaseapp.com",
    projectId: "instello-5ed0e",
    storageBucket: "instello-5ed0e.appspot.com",
    messagingSenderId: "1035049981038",
    appId: "1:1035049981038:web:4f79d51698930937fb027f",
    measurementId: "G-HMDGZL5ZHZ"
  };
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Initialize Firebase messaging
const messaging = firebase.messaging();

messaging.requestPermission()
    .then(() => {

        // Get the user's FCM token
        messaging.getToken().then((token) => {
            // Send the token to your Django backend for storage

            var csrftoken = $("[name=csrfmiddlewaretoken]").val();

            $.ajax({
                url: user_fcm_token_url,
                type: "POST",
                dataType: "json",
                data: {
                    user_email: login_user,
                    token: token,
                },
                headers:{"X-CSRFToken": csrftoken},
                success: function(data) {

                }
            })

        });
    })
    .catch((err) => {
});

messaging.onMessage(() => {
    $.toast({
        heading: "New Notification",
        text: "new notification",
        position: 'top-right',
        icon:'success',
        stack: false,
    })

});