import React from "react";
import "../styles/LoginPage.css";
import logo from "../assets/logo.png"; 

const LoginPage = () => {
return (
<div className="page-container">
{/* Top Black Banner */}
<div className="top-banner">
<img src={logo} alt="App Logo" className="logo" />

</div>
{/* Login Box */}
  <div className="login-box">
    <label className="label">Phone no.</label>
    <input type="text" placeholder="+91XXXXXXXXXX" className="input" />

    <label className="label">Password :</label>
    <input type="password" placeholder="XXXXXXXXXX" className="input" />

    <button className="login-btn">Log In</button>

    <div className="or-text">OR</div>

    <button className="signup-btn">Sign UP</button>
  </div>
</div>
);
};

export default LoginPage;