import React from 'react';
import './card.styles.css';

export const Card = (props) => (
    <div className='card-container'>
        <h5> { props.user.name }</h5>
        <p>{ props.user.email }</p>
    </div>
)

