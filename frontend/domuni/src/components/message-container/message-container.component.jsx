import React from 'react';
import './message-container.styles.css';
import { Message } from '../message/message.component'
import { SendMessageBox } from '../send-message-box/send-message-box.component'

export const MessageContainer = (props) => (
    <div className='message-container'>
        <div className = 'messages'>
            { props.messages.map(message =>
             <Message message={message} />
    
            )}
            <br></br>
           
        </div>
    </div>
)