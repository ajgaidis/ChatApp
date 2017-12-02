$(document).ready(function() {

        var socket = io.connect('http://' + document.domain + ':' + location.port);


        socket.on('message', function(msg) {
            $("#messages").append('<li>' + msg.sender + ': ' + msg.message + '</li>');
        });

        // click event on send button
        $('#sendbutton').on('click', function() {
            var message = $('#messageContent').val();
            var recipient = $('#receiver').val();
            socket.send({'message': message, 'recipient': recipient});
            $('#messageContent').val('');
        });

    });