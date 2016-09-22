var ClientStatus = React.createClass({
            render: function() {
                var current_date = new Date();
                var date_last_exchange = new Date(Date.parse(this.props.Last_exchange));
                var date_last_in = new Date(Date.parse(this.props.Data_posl_zagr));
                var date_last_out = new Date(Date.parse(this.props.Data_posl_vigr));
                var r_date = new Date(current_date - date_last_exchange);
                var style_row  = {};
                var have_error = false;
                //var style_table = {fontSize: '10px'};
                //var style_table = {};
                var date_last_exchange_string ="";
                var date_last_vigr_string ="";
                var date_last_zagr_string ="";

                if (date_last_exchange.getFullYear() == current_date.getFullYear() && date_last_exchange.getMonth() == current_date.getMonth() && date_last_exchange.getDate() == current_date.getDate()){
                    date_last_exchange_string = ""+date_last_exchange.toLocaleTimeString();
                }
                else{
                    date_last_exchange_string = date_last_exchange;
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
                if (r_date.getMinutes() > 20){
                    var style = { backgroundColor: 'red' };
                }
                else{
                    var style = { };
                };

                //проверка явных косяков
                if ((this.props.Rezult_posl_zagr == "Нет")||(this.props.Rezult_posl_vigr == "Нет")){
                    style_row = {backgroundColor: '#F3B9B9'};
                    have_error = true;
                    if(this.props.Rezult_posl_zagr == "Нет"){
                        var style_z = {backgroundColor: '#F68888', fontSize: '10px'};
                    }else{
                        var style_v = {backgroundColor: '#F68888', fontSize: '10px'};
                    }

                }else{
                    style_row = {};
                    have_error = false;
                };

                if (have_error){
                     return (
                        <tr style={style_row}>
                        <td> <b>{this.props.uzelib} </b></td>
                        <td style={style_z}> {this.props.Rezult_posl_zagr}
                             <br></br>
                             {date_last_zagr_string}
                             <br></br>
                             {this.props.Comment_zagruzka}
                        </td>
                        <td style={style_v}> {this.props.Rezult_posl_vigr}
                            <br></br>
                            {date_last_vigr_string}
                            <br></br>
                             {this.props.Comment_vigruzka}
                        </td>
                        <td style={style}> {date_last_exchange_string}

                         </td>
                        </tr>
                );
                }else{
                     return (
                        <tr style={style_row}>
                        <td> {this.props.uzelib} </td>
                        <td> {this.props.Rezult_posl_zagr}
                                &emsp;
                             {date_last_zagr_string}
                        </td>
                        <td> {this.props.Rezult_posl_vigr}
                                &emsp;
                            {date_last_vigr_string}
                        </td>
                        <td style={style}> {date_last_exchange_string}

                         </td>
                        </tr>
                );
                }

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

                                 <table className="table" style={style_table}>
                                    <tr>
                                    <td><b>Узел ИБ</b></td>
                                    <td><b>Загрузка</b></td>
                                    <td><b>Выгрузка</b></td>
                                    <td><b>Получение данных</b></td>
                                    </tr>
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
                                 </table>
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