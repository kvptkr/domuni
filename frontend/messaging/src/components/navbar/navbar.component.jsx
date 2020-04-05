import React from 'react';

export const Navbar= (props) => (
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
        <a class="navbar-item" href="http://www.domuni.com.s3-website-us-east-1.amazonaws.com/">
        Domuni
        </a>
    </div>
    <div class="navbar-end">
        <div class="navbar-item">
        <div class="buttons">
            <a class="button is-info" href="http://www.domuni.com.s3-website-us-east-1.amazonaws.com/">
            <strong>Messages &nbsp;  </strong>
            </a>
            <a class="button is-light" href="http://www.domuni.com.s3-website-us-east-1.amazonaws.com/">
            Listing &nbsp;   
            </a>
            <a class="button is-light" href="http://www.domuni.com.s3-website-us-east-1.amazonaws.com/">
            Logout 
            </a>
        </div>
        </div>
    </div>
</nav>
)