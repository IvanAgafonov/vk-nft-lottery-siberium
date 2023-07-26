import React from 'react';
import PropTypes from 'prop-types';
import './Timer.css';

import { Panel, PanelHeader, Header, Button, Group, Cell, Div, Avatar } from '@vkontakte/vkui';


const Home = ({ id, go, fetchedUser }) => (
	<Panel id={id}>
		<PanelHeader>Лотерея NFT</PanelHeader>
		{fetchedUser &&
		<Group header={<Header mode="secondary">Добро пожаловать</Header>}>
			<Cell
				before={fetchedUser.photo_200 ? <Avatar src={fetchedUser.photo_200}/> : null}
				subtitle={fetchedUser.city && fetchedUser.city.title ? fetchedUser.city.title : ''}
			>
				{`${fetchedUser.first_name} ${fetchedUser.last_name}`}

			</Cell>
		</Group>}

		<Group header={<Header mode="secondary">Навигация</Header>}>
			<Div>
				<Button stretched size="l" mode="secondary" onClick={go} data-to="mint">
					Получить билет
				</Button>
				<Button stretched size="l" mode="secondary" onClick={go} data-to="items">
					Показать билеты
				</Button>
			</Div>
			<p>До розыгрыша:</p>
			<div id="timer"></div>
		</Group>
	</Panel>
);


function updateTimer() {
	var future  = Date.parse("December 11, 2023 11:30:00");
	var now     = new Date();
	var diff    = future - now;
  
	var years = Math.floor( diff / (1000*60*60*24*365) );
	var days  = Math.floor( diff / (1000*60*60*24) );
	var hours = Math.floor( diff / (1000*60*60) );
	var mins  = Math.floor( diff / (1000*60) );
	var secs  = Math.floor( diff / 1000 );
  
	var y = years;
	var d = days  - years * 365;
	var h = hours - days  * 24;
	var m = mins  - hours * 60;
	var s = secs  - mins  * 60;
  
	document.getElementById("timer")
	  .innerHTML =
		// '<div>' + y + '<span>years</span></div>' +
		'<div>' + d + '<span>days</span></div>' +
		'<div>' + h + '<span>hours</span></div>' +
		'<div>' + m + '<span>minutes</span></div>' +
		'<div>' + s + '<span>seconds</span></div>' ;
  }
setInterval(updateTimer, 1000 );

Home.propTypes = {
	id: PropTypes.string.isRequired,
	go: PropTypes.func.isRequired,
	fetchedUser: PropTypes.shape({
		photo_200: PropTypes.string,
		first_name: PropTypes.string,
		last_name: PropTypes.string,
		id: PropTypes.number,
		city: PropTypes.shape({
			title: PropTypes.string,
		}),
	}),
};

export default Home;
