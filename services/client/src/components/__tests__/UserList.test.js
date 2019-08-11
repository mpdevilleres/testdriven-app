import React from 'react';
import {shallow} from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UserList';

const users = [
    {
        active: true,
        email: 'marc@gmail.com',
        id: 1,
        username: 'marc'
    },
    {
        active: true,
        email: 'philippe@gmail.com',
        id: 2,
        username: 'philippe'
    }
];

test('UsersList renders properly', () => {
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.children).toBe('marc');
});

test('UsersList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});