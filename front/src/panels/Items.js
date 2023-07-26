import React from 'react';
import PropTypes from 'prop-types';

import { Panel, PanelHeader, PanelHeaderBack, Group, FormLayout, FormItem, Input, Button } from '@vkontakte/vkui';

import './Items.css';



const Items = props => (
	<Panel id={props.id}>
        <PanelHeader
			before={<PanelHeaderBack onClick={props.go} data-to="home"/>}
		>
			Items
		</PanelHeader>

        <Group>
          <FormLayout>
            <FormItem
              htmlFor="Address"
              top="Address"
            >
              <Input
                id="address"
                type="Address"
                name="Address"
              />
            </FormItem>
            <FormItem>
              <Input type="submit" value="Показать" onClick={Items.getAll}/>
            </FormItem>

          </FormLayout>
          <Button size="l" align='center' stretched onClick={Items.refresh}>
              Обновить метаданные
            </Button>
          
          </Group>
	</Panel>
);

Items.refresh = function (e) {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', 'https://somesasdsad.ydns.eu:5000/api/refresh', false);
  xhr.send(null);
  if (xhr.status === 201 || xhr.status === 200) {
      console.log(xhr.responseText);
  } else {
     throw new Error('Request failed: ' + xhr.statusText);
  }
}


Items.getAll = function (e) {
    var addres = document.querySelector("#address").value;
  
    var nfts = document.querySelectorAll(".nft");

    for (let i = 0; i < nfts.length; i++) {
        nfts[i].remove();
    }

    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://somesasdsad.ydns.eu:5000/api/token?address=' + addres, false);
    xhr.send(null);
    if (xhr.status === 201 || xhr.status === 200) {
        console.log(xhr.responseText);
        var jsonResponse = JSON.parse(xhr.responseText);
        console.log(jsonResponse);
    } else {
       throw new Error('Request failed: ' + xhr.statusText);
    }

    for (let i = 0; i < jsonResponse.items.length; i++) {
        console.log(jsonResponse.items[i].tokenId);

        var div = document.createElement("div");
        div.setAttribute('class', 'nft');
    
        var img = document.createElement("img");
        img.setAttribute('class', 'Items');
        img.setAttribute('src', 'https://ipfs.io/ipfs/' + jsonResponse.items[i].metadata.image.split("//")[1]);
        img.setAttribute('alt', 'Nft');
    
        var paragraph = document.createElement("p");
        paragraph.setAttribute('align', 'center');
    
        var text_id = document.createTextNode("Token id: " + jsonResponse.items[i].tokenId);
        paragraph.appendChild(text_id);
    
        paragraph.appendChild(document.createElement("br"));
    
        var text_desc = document.createTextNode(jsonResponse.items[i].metadata.description);
        paragraph.appendChild(text_desc);
    
        div.appendChild(img);
        div.appendChild(paragraph);
    
        var element = document.querySelector("#items").querySelector(".vkuiPanel__in-after");
        element.parentNode.insertBefore(div, element);

      }
    
  }

Items.propTypes = {
	id: PropTypes.string.isRequired,
	go: PropTypes.func.isRequired,
};

export default Items;
