'use strict';
/**
 * controller for Messages
 */

app.controller('ChatCtrl', function ($scope, $rootScope, socketIO) {
    $scope.user = $rootScope.user;

    var load = function () {
        $scope.user = $rootScope.user;
        $scope.noAvatarImg = "static/assets/images/default-user.png";
        $scope.usersList = [];
        $scope.otherIdUser = "";
        $scope.otherName = "";
        $scope.chat = [];
        if ($scope.user) {
            $scope.usersList = $scope.user.contact_list;
            $scope.selfIdUser = $scope.user._id;
            socketIO.emit('init', {"id": $scope.selfIdUser});
        }
    }

    $scope.setChat = function (id, firstname, lastname) {
        $scope.otherIdUser = id;
        $scope.otherName = firstname + " " + lastname;

        socketIO.emit('join', {'name': $scope.user.name,
        'id': $scope.selfIdUser,
        'otherId': $scope.otherIdUser});
    }

    $scope.addUser = function (user) {
        $scope.usersList.push(user);
    }

    var receiveMessage = function (data) {
        var newMessage = {
            "date": data.date,
            "content": data.data,
            "idUser": data.send_address,
            "idOther": data.recip_address,
            "avatar": data.avatar
        };
        $scope.chat.push(newMessage);
        $scope.chatMessage = '';
    };

    socketIO.on('send_message', function (data) {
        receiveMessage(data);
    })

    socketIO.on('last_messages', function (data) {
        data = JSON.parse(data);
        for (var message in data) {
            receiveMessage(data[message]);
        }
    })

    $scope.sendMessage = function () {
        var newMessage = {
            "date": new Date(),
            "content": $scope.chatMessage,
            "idUser": $scope.selfIdUser,
            "idOther": $scope.otherIdUser,
            "avatar": $scope.noAvatarImg,
            "files": null
        };
        if (newMessage.content != '') {
            $scope.chat.push(newMessage);
            socketIO.emit('send_message', newMessage);
        }
        $scope.chatMessage = '';
    };

    $rootScope.$on('loadChat', function(event, data) {
        load();
    });

    load();
});
