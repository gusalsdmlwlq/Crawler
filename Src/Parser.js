const puppeteer = require('puppeteer');

// var url_ = process.argv[2];
// var url = url_.split(" ")[0];
// var mode = url_.split(" ")[1];

function printarray(array){
	for(var i=0; i<array.length; i++){
		if(typeof(array[i]) == "string") process.stdout.write(array[i].replace(/\n/gi, " ")+"\n");
		else process.stdout.write(""+array[i]+"\n");
	}
}

function show(array){
	for(var i=0; i<array.length; i++){
		if(typeof(array[i]) == "string"){
			printarray(array);
			return;
		}
		else show(array[i]);
	}
}

async function parse(url_){
	var url = url_.split(" ")[0];
	var mode = url_.split(" ")[1];
	const browser = await puppeteer.launch({
	    args: ["--no-sandbox", "--disable-web-security", "--user-data-dir=data", '--enable-features=NetworkService', '--start-fullscreen',  '--window-size=1920,1080']
	});
	const page = await browser.newPage();
	await page.on("error");
	await page.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36");
	await page.goto(url);
	await page.waitFor(3000);
	const nodes = await page.evaluate((url,mode) => {
		var bodywidth = document.body.scrollWidth;
		var bodyheight = document.body.scrollHeight;
		var y_max = 0;
		var y_bottom = 0;
		function getpos(node) {
			var position = new Object;
			position.x = 0;
			position.y = 0;
			position.w = node.offsetWidth;
			if(node){
				position.x = node.offsetLeft + node.clientLeft;
				position.y = node.offsetTop + node.clientTop;
				if(node.offsetParent) {
					var parentpos = getpos(node.offsetParent);
					position.x += parentpos.x;
					position.y += parentpos.y;
					if(["SPAN","EM", "B"].includes(node.nodeName)){
						var parent_ = getpos(node.parentNode);
						if(position.x+position.w > parent_.x+parent_.w)  position.x = parent_.x;
					}
				}
			}
			return position;
		}
		function checkad(link){
			if(link == "#") return false;
			if(link[0] == "/") return false;
			let link_machine = link.split('.')[0].split('/')[2];
			let link_domain = link.split('.')[1];
			let url_machine = url.split('.')[0].split('/')[2];
			let url_domain = url.split('.')[1];
			if(link_domain != url_domain || link_machine != url_machine) return true;
			else return false;
		}

		function checkdiv(node){ //ad => return 0
			let childnodes = node.childNodes;
			for(var i=0; i<childnodes.length; i++){
				if(["DIV", "P", "SPAN"].includes(childnodes[i].nodeName)) continue;
				if(childnodes[i].nodeName == "A"){
					let href = childnodes[i].getAttribute("href");
					if(href != "#") return 0;
					if(checkad(href) == true) return 0;
				}
				if(checkdiv(childnodes[i]) == 0) return 0;
			}
			return 1;
		}

		function recur(root, indent, is_link, is_ad, framewidth, frameheight){
			let contents = root.childNodes;
			let result = new Array();
			let attributes = new Array(); //(type, content, x, y, w, h, fontsize, bg_color, indent) : node의 attribute
			let childindent = indent;
			let isad = is_ad;
			for(var i=0; i<contents.length; i++){
				attributes = new Array();
				let node = contents[i];
				let newframewidth = framewidth;
				let newframeheight = frameheight;
				if(["SCRIPT", "#comment", "STYLE", "NOSCRIPT"].includes(node.nodeName)) continue;
				if(node.nodeValue != null){
					if(node.nodeValue.trim().length != 0 && node.nodeName == "#text" && isad == false){ //text node 체크
						attributes.push("text");
						attributes.push(node.nodeValue.trim());
						if(node.parentNode.innerHTML != node.nodeValue){ //태그가 없는 text node 체크
							let spantext = document.createTextNode(node.nodeValue);
							let insertspan = document.createElement('span');
							insertspan.appendChild(spantext);
							node.parentNode.insertBefore(insertspan, node);
							node.parentNode.removeChild(node);
							node = spantext;
							childindent += 1;
						}
						node = node.parentNode;
						let x = getpos(node).x + node.offsetWidth / 2 + framewidth;
						let y = getpos(node).y + node.clientTop + node.offsetHeight / 2 + frameheight;
						if(x <= 0 || y <= 0) continue;
						if(y_bottom != 0 && y >= y_bottom) continue;
						attributes.push(x);
						attributes.push(y);
						let w = node.offsetWidth;
						let h = node.offsetHeight;
						if(w <= 1.0 || h <= 1.0) continue;
						if(y + h/2 > y_max) y_max = y + h/2;
						attributes.push(w);
						attributes.push(h);
						let size = window.getComputedStyle(node,null).getPropertyValue('font-size');
						size = size.split('p')[0]*1
						attributes.push(size);
						if(size <= 0) continue;
						let bgcolor = window.getComputedStyle(node,null).getPropertyValue('background-color');
						attributes.push(bgcolor);
						attributes.push(childindent);
					}
				}
				else{
					if(window.getComputedStyle(node,null).getPropertyValue('display') == "none") continue;
					let position = window.getComputedStyle(node,null).getPropertyValue('position');
					let z_index = window.getComputedStyle(node,null).getPropertyValue('z-index');
					if(node.nodeName == "IFRAME"){
						newframewidth = framewidth + getpos(node).x;
						newframeheight = frameheight + getpos(node).y;
						node = node.contentWindow.document.body;
						if(node == null){
							continue;
						}
					}
					else if(node.nodeName == "IMG"){ //img node 체크
						if(isad == false){
							attributes.push("img");
							attributes.push(node.src);
							let x = getpos(node).x + node.offsetWidth / 2 + framewidth;;
							let y = getpos(node).y + node.offsetHeight / 2 + frameheight;
							if(x <= 0 || y <= 0) continue;
							if(y_bottom != 0 && y >= y_bottom) continue;
							attributes.push(x);
							attributes.push(y);
							let w = node.offsetWidth;
							let h = node.offsetHeight;
							if(w <= 1 || h <= 1) continue;
							attributes.push(w);
							attributes.push(h);
							attributes.push(0);
							attributes.push("rgba(0, 0, 0, 0)");
							attributes.push(childindent);
						}
					}
					if(node.childNodes != null && position != "fixed" && (z_index == "auto" || z_index < 10000)){
						if(mode == 2){
							let islink = is_link;
							if(node.nodeName == "A"){
								let href = node.getAttribute("href");
								if(href != "#") islink = true;
								if(href == null || checkad(href) == true) isad = true;
							}
							if(node.nodeName == "UL") continue;
							if(["DIV", "P", "SPAN"].includes(node.nodeName)){ 
								let is_skip = 0;
								node_class = node.getAttribute("class");
								node_id = node.getAttribute("id");
								let exp_bottom = [/comment/,/tag/,/bottom/,/ccl/];
								let exp = [/category/,/plugin/,/player/];
								for(var j=0; j<exp_bottom.length; j++){ //bottom 갱신
									if(exp_bottom[j].test(node_class) || exp_bottom[j].test(node_id)){
										is_skip = 1;
										let y = getpos(node).y + node.offsetHeight / 2 + frameheight;
										let w = node.offsetWidth;
										let h = node.offsetHeight;
										if((y_bottom == 0 || (y_bottom != 0 && y_bottom > y)) && w > 0 && h > 0) y_bottom = y;
										break;
									}
								}
								for(var j=0; j<exp.length; j++){ //category, plugin, player 제거
									if(exp[j].test(node_class) || exp[j].test(node_id)){
										is_skip = 1;
										break;
									}
								}
								if(is_skip == 1) continue;
							}
							result.push(recur(node,indent+1,islink,isad,newframewidth,newframeheight));
							isad = is_ad;
						}
						else if(mode == 3){
							if(["DIV", "P", "SPAN"].includes(node.nodeName) && checkdiv(node) == 0) continue;
							if(node.nodeName == "UL") continue;
							result.push(recur(node,indent+1,false,false,newframewidth,newframeheight));
						}
						else{
							let islink = is_link;
							if(node.nodeName == "A"){
								let href = node.getAttribute("href");
								if(href != "#") islink = true;
								if(href == null || checkad(href) == true) isad = true;
							}
							result.push(recur(node,indent+1,islink,isad,newframewidth,newframeheight));
							isad = is_ad;
						}
					}
				}
				result.push(attributes);
			}
			return result;
		}
		body = document.querySelector("body");
		if(bodyheight <= 1000) return [recur(body,0,false,0,0,0), 1200, y_max];
		return [recur(body,0,false,0,0,0), bodywidth, bodyheight];
	}, url,mode);
	await browser.close();
	await show(nodes);
	await process.stdout.write(""+nodes[nodes.length-2]+"\n");
	await process.stdout.write(""+nodes[nodes.length-1]+"\n");
	await process.stdout.write(""+url+"\n");
}
// parse(url,mode);
process.stdin.setEncoding("utf-8");
process.stdout.setEncoding("utf-8");
process.stdin.on('readable', () => {
	var url = process.stdin.read();
	if(url){
		parse(url);
	}
});