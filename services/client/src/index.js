import React, {useState, useEffect} from 'react';
import ReactDOM from 'react-dom';

import axios from 'axios';
import UsersList from "./components/UserList";
import AddUser from "./components/AddUser";

const App = () => {
    const [users, setUsers] = useState([]);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');

    const addUser = (event) => {
        event.preventDefault();
        const payload = {username, email};
        axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, payload)
            .then(res => {
                console.log(res);
                setUsers([...users, {...payload, id: Math.random()}]);
            })
            .catch(err => {
                console.log(err);
            });
    };

    const handleOnChangeUsername = (event) => {
        setUsername(event.target.value);
    };

    const handleOnChangeEmail = (event) => {
        setEmail(event.target.value);
    };

    const getUsers = () => {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
            .then(res => {
                setUsers(res.data.data.users);
            })
            .catch(err => {
                console.log(err);
            })
    };

    useEffect(() => {
        getUsers();
    }, []);

    return (
        <section className="section">
            <div className="container">
                <div className="columns">
                    <div className="column is-half">
                        <br/>
                        <h1 className="title is-1">All Users</h1>
                        <hr/>
                        <br/>
                        <AddUser
                            addUser={addUser}
                            username={username} setUsername={setUsername}
                            email={email} setEmail={setEmail}
                            handleOnChangeUsername={handleOnChangeUsername}
                            handleOnChangeEmail={handleOnChangeEmail}
                        />
                        <hr/>
                        <br/>
                        <UsersList users={users}/>
                    </div>
                </div>
            </div>
        </section>
    )
};

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);