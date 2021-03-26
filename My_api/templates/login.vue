<template>
  <div class="container">
    <div class="login-box">
      <div class="apple-btn login-apple">
        <li class="red-btn"></li>
        <li class="yellow-btn"></li>
        <li class="green-btn"></li>
      </div>
      <div class="title">Login</div>
      <div class="input">
        <label for="login-user"></label
        ><input type="text" id="login-user" placeholder="Input your username" />
      </div>
      <div class="input">
        <label for="login-password"></label
        ><input
          type="password"
          id="login-password"
          placeholder="Input your password"
        />
      </div>
      <div class="btn login-btn" id="login" v-on:click="handleLogin">
        <span>登录</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
 name: 'login',

}
</script>

<style>
* {
  padding: 0px;
  margin: 0px;
}

html,
body {
  height: 100%;
  width: 100%;
  background-image: linear-gradient(120deg, #487eb0, #fbc531);
  overflow: hidden;
}

.container {
  position: absolute;
  height: 350px;
  width: 600px;
  background-color: rgba(255, 255, 255, 0.9);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -30%);
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(17, 39, 59, 0.8);
  border: 1px solid rgba(17, 39, 59, 1);
  overflow: hidden;
  box-sizing: border-box;
  transition: 1s;
}
.btn:hover {
  background-color: #4d3253;
}

.title {
  margin-top: 10px;
  position: relative;
  height: 40px;
  width: 100%;
  font-size: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 3px;
  transition: 0.4s;
}
.login-box .title {
  color: white;
  text-shadow: 0px 0px 7px rgba(255, 255, 255, 0.9);
}

.input {
  width: 400px;
  height: 45px;
  position: relative;
  margin: 40px auto;
  /* border-radius: 45px;
    overflow: hidden; */
}

input {
  position: relative;
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  /* box-sizing: border-box; */
  padding-left: 15px;
  font-size: 16px;
  background-color: rgba(255, 255, 255, 0.4);
  border-radius: 45px;
  transition: 0.4s;
}

.login-box input:focus {
  box-shadow: 0 0 10px rgba(1, 1, 1, 0.8);
}

.btn {
  height: 50px;
  width: 160px;
  position: relative;
  margin: -10px auto;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: 0.4s;
}

.login-box input {
  caret-color: white;
  color: rgba(255, 255, 255, 0.8);
}

.login-box {
  position: absolute;
  height: 100%;
  width: 100%;
  background-color: rgba(17, 39, 59, 0.8);
  transition: 0.4s;
  z-index: 1;
  transform-origin: 0 100%;
}

/* 注册框样式 */
.sign-box {
  position: absolute;
  height: 100%;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  transform-origin: 0 100%;
  transform: rotate(90deg);
  transition: 0.4s;
  z-index: 1;
}

.sign-box .title {
  text-shadow: 0 0 10px rgba(200, 200, 200, 0.8);
  font-weight: 500;
}

.sign-change {
  background-color: rgba(17, 39, 59, 0.8);
}

.toLogin {
  color: white;
}

.sign-box input {
  box-shadow: 0 0 3px black;
}

.sign-box .btn {
  color: #1e90ff;
  background-color: rgba(200, 200, 200, 0.1);
  transition: 0.5s;
}

.sign-box .btn:hover {
  color: white;
  background-color: #1e90ff;
}

/* Mac 按钮样式及特效 */
.apple-btn {
  position: absolute;
  height: 15px;
  width: 65px;
  top: 3px;
}
.apple-btn li {
  list-style: none;
  position: relative;
  height: 15px;
  width: 15px;
  border-radius: 15px;
  opacity: 0;
}

.login-apple li {
  left: 5px;
  float: left;
}

.sign-apple li {
  right: 5px;
  float: right;
}

.sign-apple {
  right: 5px;
}

li:nth-child(2) {
  margin: 0px 2px;
}

.red-btn {
  background-color: red;
  transition: 0.3s;
  transform: translate(0, -50%);
}

.yellow-btn {
  background-color: orange;
  /* transition-delay: .2s; */
  transition: 0.6s;
  transform: translate(0, -50%);
}

.green-btn {
  background-color: rgb(15, 136, 15);
  /* transition-delay: .3s; */
  transition: 0.9s;
  transform: translate(0, -50%);
}

.container:hover .red-btn {
  opacity: 1;
  transform: translate(0, 0);
}
.container:hover .yellow-btn {
  opacity: 1;
  transform: translate(0, 0);
}
.container:hover .green-btn {
  opacity: 1;
  transform: translate(0, 0);
}
</style>
