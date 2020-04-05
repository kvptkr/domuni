import React, { Component } from 'react';
import { CardList } from "./components/card-list.component";
import { SearchBox } from "./components/search-box.component";
import { Navbar } from "./components/navbar/navbar.component";
import { MessageContainer } from "./components/message-container/message-container.component";
import "bootstrap/dist/css/bootstrap.css";
import './App.css';
import { SendMessageBox } from './components/send-message-box/send-message-box.component';



class App extends Component {
  constructor() {
    
    super();
    var firstMessage ={
        text: "I'm interested in touring your property",
        timestamp: "30/03/2020",
        sender: 'Leanne Graham'
    }

    this.state = {
      users: [],
      currentConversationPartner: 1,
      messages: [firstMessage
      ],
      searchField: '',
      messageBox: '',
    };
  }
  componentDidMount(){
    fetch('https://jsonplaceholder.typicode.com/users')
    .then(response => response.json())
    .then(users => this.setState({users: users}));
       
  }
 sendMsg=() => {
    var messageText=document.getElementsByName('sendMessageBox')[0].value
    document.getElementsByName('sendMessageBox')[0].value = ''
    var now = new Date();
    var nowString = now.toUTCString();

    var newMessage={
        text: messageText,
        timestamp: nowString,
        sender: 'Feridun Hamdallahpur'
    }
    
    this.setState({
      messages: [...this.state.messages, newMessage]})

    
      /*
        fetch('https://cors-anywhere.herokuapp.com/http://domuni.us-east-1.elasticbeanstalk.com/create-message', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        lessor_id: lessor_id,
        subletter_id: subletter_id,
        text: messageText,
        lessor_sent: true,
      })
    })
      */
   
    
  }
  
  render(){
    const { users, searchField, messages  } = this.state;
    const filteredUsers = users.filter(user =>
        user.name.toLowerCase().includes(searchField.toLowerCase())
      )
    return (
      <div className="App">
      <Navbar />
      <div>
        <center>
        < SearchBox placeholder='search users' handleChange= {e => this.setState({searchField: e.target.value})}/>
        </center>
        <div class="container">
          <div class="row">
            <div class="col-sm-3">
            < CardList users = { filteredUsers } />
            </div>
            <div class="col-sm-9">
              < MessageContainer messages= {messages}/>
              < SendMessageBox onClick={ this.sendMsg} />
              <button type="button" class="btn btn-outline-secondary" onClick={this.sendMsg}>Send Message</button>
            </div>
          </div>
        </div>
        </div>
      </div>
    );
  }
}


export default App;
