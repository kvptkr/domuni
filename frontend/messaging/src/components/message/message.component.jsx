import React from 'react';
import './message.styles.css';

export const Message = (props) => (
    <div className='card-container'>
        <p>Sent By: { props.message.sender } </p>
        <h5> { props.message.text }</h5>
        <p> { props.message.timestamp}</p>
    </div>
)