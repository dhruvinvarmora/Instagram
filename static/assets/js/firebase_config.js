const firebaseConfig = {
        apiKey: "{{ firebase_config.apiKey }}",
        authDomain: "{{ firebase_config.authDomain }}",
        projectId: "{{ firebase_config.projectId }}",
        storageBucket: "{{ firebase_config.storageBucket }}",
        messagingSenderId: "{{ firebase_config.messagingSenderId }}",
        appId: "{{ firebase_config.appId }}",
        measurementId: "{{ firebase_config.measurementId }}"
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