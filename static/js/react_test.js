var ClientStatus = React.createClass({
            render: function() {
                var current_date = new Date();
                var date_last_exchange = new Date(Date.parse(this.props.Last_exchange));
                var date_last_in = new Date(Date.parse(this.props.Data_posl_zagr));
                var date_last_out = new Date(Date.parse(this.props.Data_posl_vigr));
                var r_date = new Date(current_date - date_last_exchange);
                var style_row  = {};
                var have_error = false;
                var style_name = {fontSize: '11px'};
                //var style_table = {};
                var date_last_exchange_string ="";
                var date_last_vigr_string ="";
                var date_last_zagr_string ="";


                if (date_last_exchange.getFullYear() == current_date.getFullYear() && date_last_exchange.getMonth() == current_date.getMonth() && date_last_exchange.getDate() == current_date.getDate()){
                    date_last_exchange_string = ""+date_last_exchange.toLocaleTimeString();
                }
                else{
                    date_last_exchange_string = ""+date_last_exchange.toLocaleDateString() + " " + date_last_exchange.toLocaleTimeString();
                };


                if (date_last_out){
                if (date_last_out.getFullYear() == current_date.getFullYear() && date_last_out.getMonth() == current_date.getMonth() && date_last_out.getDate() == current_date.getDate()){
                    date_last_vigr_string = ""+date_last_out.toLocaleTimeString();
                }
                else{
                    date_last_vigr_string = this.props.Data_posl_vigr;
                };}


                if (date_last_in){
                if (date_last_in.getFullYear() == current_date.getFullYear() && date_last_in.getMonth() == current_date.getMonth() && date_last_in.getDate() == current_date.getDate()){
                    date_last_zagr_string = ""+date_last_in.toLocaleTimeString();
                }
                else{
                    date_last_zagr_string = this.props.Data_posl_zagr;
                };}




                //проверка на то что данные вообще к нам приходят
                if ((r_date.getMinutes() > 20)||(r_date.getDate() >1)){
                    var style_ping = { color: 'red', fontSize: '12px' };
                }
                else{
                    var style_ping = { color: 'green', fontSize: '12px' };
                };


                //проверка явных косяков
                 have_error = false;
                 if(this.props.Rezult_posl_zagr == "Нет"){
                    var style_row_in = {color: '#F68888', fontSize: '12px'};
                    have_error = true;
                 }else{
                    var style_row_in = {fontSize: '12px'};
                 }
                  if(this.props.Rezult_posl_vigr == "Нет"){
                    var style_row_out = {color: '#F68888', fontSize: '12px'};
                    have_error = true;
                 }else{
                    var style_row_out = {fontSize: '12px'};
                 }


                if (have_error){
                    var picture_path = "static/img/db_er.png";
                }else{
                    var picture_path = "static/img/db.png";
                }

                return(

                        <div className="col-xs-6 col-md-2">
                            <div className="thumbnail">
                            <p>
                                <span className="glyphicon glyphicon-signal" aria-hidden="true" style={style_ping}> {date_last_exchange_string}</span>
                            </p>

                                <img src={picture_path} width="60" height="80"></img>

                                <div class="caption">
                                    <div style={style_name}>{this.props.uzelib}</div>
                                    <p>
                                        <span className="glyphicon glyphicon-log-in" aria-hidden="true" style={style_row_in}> {date_last_zagr_string}</span>
                                     </p>
                                     <p>
                                        <span className="glyphicon glyphicon-log-out" aria-hidden="true" style={style_row_out}> {date_last_vigr_string}</span>
                                    </p>

                                </div>
                            </div>
                        </div>


                );
            }
        });

var Client = React.createClass({
            render: function() {
                var style_table = {fontSize: '12px'};
                return (
                    <div className="client">
                        <div className="client-info">
                            <div className="panel panel-default">
                                <div className="panel-heading">
                                    <h3 className="panel-title">{this.props.name}</h3>
                                </div>

                                    <div className="row">
                                         {
                                            this.props.status_array.map(function(el) {
                                             return <ClientStatus
                                                key ={el.uzelib}
                                                uzelib={el.uzelib}
                                                Rezult_posl_zagr={el.Rezult_posl_zagr}
                                                Rezult_posl_vigr={el.Rezult_posl_vigr}
                                                Data_posl_zagr={el.Data_posl_zagr}
                                                Data_posl_vigr={el.Data_posl_vigr}
                                                Comment_zagruzka={el.Comment_zagruzka}
                                                Comment_vigruzka={el.Comment_vigruzka}
                                                Last_exchange={el.Last_exchange}
                                            />;
                                             })
                                         }
                                     </div>

                            </div>
                        </div>
                    </div>
                );
            }
        });

        var ClientList = React.createClass({
            getInitialState: function() {
                return {
                    displayedClients: []
                };
            },

            componentDidMount: function() {
                var namespace = '/test';

                this.socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
                this.socket.on('my response', this.socket_on);
            },

            socket_on: function(msg) {
                $('#footerInfo').html('Received #' + msg.count + ': ' + msg.data);

                if (msg.clients) {

                    var jsonObj = JSON.parse(msg.clients);
                    this.setState({displayedClients: jsonObj});
                }
                else{
                    this.setState({displayedClients: []});
                }
            },

            render: function() {
                return (
                    <div className="clients">
                        <div className="clients-list">
                            {

                               this.state.displayedClients.map(function(el) {
                                    return <Client
                                        key={el.client.client_id}
                                        name={el.client.client_name}
                                        status_array={el.status_array}
                                    />;
                               })
                            }
                        </div>
                    </div>
                );
            }
        });

        ReactDOM.render(
            <ClientList />,
            document.getElementById("content")
        );