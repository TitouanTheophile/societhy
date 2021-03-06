 app.controller('userOverviewCtrl', function($scope, $http, $timeout) {
 	var ctrl = this;

//Load facebook SDK
window.fbAsyncInit = function() {
	FB.init({
		appId      : '1774766892791379',
		xfbml      : true,
		version    : 'v2.8'
	});
	FB.AppEvents.logPageView();
};

(function(d, s, id){
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) {return;}
	js = d.createElement(s); js.id = id;
	js.src = "//connect.facebook.net/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

ctrl.fb_connect = function (argument) {
	FB.login(function(response) {

		if (response.authResponse) 
		{
            access_token = response.authResponse.accessToken; //get access token
            user_id = response.authResponse.userID; //get FB UID
            console.log("token : " + access_token);
            console.log("user_id : " + user_id);
            FB.api('/me', {fields: 'email, name, picture'} ,function(response) 
            {
                console.log("name : " + response.name);
                console.log("email : " + response.email);
                console.log("photo url " + response.picture.data.url);

                newPhoto = angular.element(document.querySelector('#newPhoto'));
                newPhoto.html('<img src="'+ response.picture.data.url + '">')           

            });

        } else {
            //user hit cancel button
            console.log('User cancelled login or did not fully authorize.');

        }
    }, {
    	scope: 'public_profile,email'
    });

}


});