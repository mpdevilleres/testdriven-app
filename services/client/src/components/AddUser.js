import React from 'react';

const AddUser = (
    {
        addUser,
        username, handleOnChangeUsername,
        email, handleOnChangeEmail

    }) => {
    return (
        <form onSubmit={addUser}>
            <div className="field">
                <input
                    name="username"
                    className="input is-large"
                    type="text"
                    placeholder="Enter an username"
                    required
                    value={username}
                    onChange={handleOnChangeUsername}
                />
            </div>
            <div className="field">
                <input
                    name="email"
                    className="input is-large"
                    type="email"
                    placeholder="Enter an email"
                    required
                    value={email}
                    onChange={handleOnChangeEmail}
                />
            </div>
            <input
                type="submit"
                className="button is-primary is-large is-fullwidth"
                value="Submit"
            />
        </form>
    )
};

export default AddUser;