$(document).ready(function(){
            namespace = '/test'; // change to an empty string to use the global namespace

            // the socket.io documentation recommends sending an explicit package upon connection
            // this is specially important when using the global namespace
            var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

            // event handler for server sent data
            // the data is displayed in the "Received" section of the page
            socket.on('my response', function(msg) {
                $('#footerInfo').html('Received #' + msg.count + ': ' + msg.data);

                if (msg.clients) {

                    var jsonObj = $.parseJSON(msg.clients);
                    if ($.isArray(jsonObj)) {
                        for (i=0; i<jsonObj.length; i++){
                            $('#test11').html(jsonObj[i].client.client_name);
                        }
                    }

                }
            });

            // event handler for new connections
            socket.on('connect', function() {
                socket.emit('my event', {data: 'I\'m connected!'});
            });


        });