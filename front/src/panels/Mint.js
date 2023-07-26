import React, { useState, forceUpdate  }  from 'react';
import PropTypes from 'prop-types';

import { Panel, PanelHeader, PanelHeaderBack, SplitLayout, Group, FormLayout, ScreenSpinner, FormItem, Input, Button } from '@vkontakte/vkui';
import './Loading.css';




const Mint = props => {
  const [popout, setPopout] = useState(null);

  const setDoneScreenSpinner = async () => {
    setPopout(<ScreenSpinner state="loading" />);
    useState(null);
    setTimeout(() => {
      setPopout(<ScreenSpinner state="done">Успешно</ScreenSpinner>);
  
      setTimeout(clearPopout, 1000);
    }, 2000);
  };

  const mint = async (e) => {  
    var element = document.querySelector('input[type="submit"]');
    element.setAttribute("style", "background-color:green;");
    setDoneScreenSpinner();
    console.log(e.target[0].value); 
    
    var body = JSON.stringify({
      address: e.target[0].value,
      vkId: e.target[1].value
    });

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://somesasdsad.ydns.eu:5000/api/mint', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(body);
    if (xhr.status === 201 || xhr.status === 200) {
      console.log(xhr.responseText);
    } else {
      throw new Error('Request failed: ' + xhr.statusText);
    }
  }


  return(

	<Panel id={props.id}>
		<PanelHeader
			before={<PanelHeaderBack onClick={props.go} data-to="home"/>}
		>
			Mint
		</PanelHeader>
    <SplitLayout popout={popout} aria-live="polite" aria-busy={!!popout}>

    </SplitLayout>
      <Group>
          <FormLayout onSubmit={mint}>
            <FormItem
              htmlFor="Address"
              top="Address"
            >
              <Input
                id="address"
                type="Address"
                name="Address"
              />
              <input
                id="id"
                type="id"
                name="id"
                value={props.fetchedUser.id}
                hidden
              />
            </FormItem>
            <FormItem>
              <Input type="submit"/>
            </FormItem>
          </FormLayout>
          </Group>
	</Panel>
) };

Mint.propTypes = {
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

export default Mint;
