const puppeteer = require('puppeteer');

function printarray(array,bottom){ // 노드 정보를 출력
	if(array[3]*1 > bottom) return; //bottom line 아래의 노드들은 제외
	for(var i=0; i<array.length; i++){
		if(typeof(array[i]) == "string") process.stdout.write(array[i].replace(/\n/gi, " ")+"\n");
		else process.stdout.write(""+array[i]+"\n");
	}	
}

function show(array,bottom){ // 노드 정보를 출력
	for(var i=0; i<array.length; i++){
		if(typeof(array[i]) == "string"){
			printarray(array,bottom);
			return;
		}
		else show(array[i],bottom);
	}
}

function checkbottom(bottoms,height){ // bottom line 결정
	var bottom = height;
	var tags = bottoms[0];
	var ccls = bottoms[1];
	var comments = bottoms[2];
	var posts = bottoms[3];
	var tag_max = 0;
	var ccl_max = 0;
	var comment_max = 0;
	var post_max = 0;
	for(var i=0; i<tags.length; i++){
		if(tags[i] > tag_max) tag_max = tags[i];
	}
	for(var i=0; i<ccls.length; i++){
		if(ccls[i] > ccl_max) ccl_max = ccls[i];
	}
	for(var i=0; i<comments.length; i++){
		if(comments[i] > comment_max) comment_max = comments[i];
	}
	for(var i=0; i<posts.length; i++){
		if(posts[i] > post_max) post_max = posts[i];
	}
	if(tag_max > height/2 && tag_max < bottom) bottom = tag_max;
	if(ccl_max > height/2 && ccl_max < bottom) bottom = ccl_max;
	if(comment_max > height/2 && comment_max < bottom) bottom = comment_max;
	if(post_max > height/2 && post_max < bottom) bottom = post_max;
	return bottom;
}

async function parse(url_){ // url 정보를 입력 받아 페이지의 DOM tree 파싱하며 노드 정보 추출
	var url = url_.split(" ")[0]; // url
	var mode = url_.split(" ")[1]; // 타겟 페이지의 카테고리(뉴스, 블로그, 쇼핑몰)
	const browser = await puppeteer.launch({ // puppeteer 설정
	    args: ["--no-sandbox", "--disable-web-security", "--user-data-dir=data", '--enable-features=NetworkService', '--start-fullscreen',  '--window-size=1920,1080', '--disable-dev-shm-usage',"--force-color-profile=srgb|generic-rgb|color-spin-gamma24"]
	});
	const page = await browser.newPage();
	await page.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36");
	await page.goto(url,{waitUntil: "networkidle2", timeout: 60000});
	await page.waitFor(2000);
	const nodes = await page.evaluate((url,mode) => { // url 정보들을 nodes 변수에 저장
		var bodywidth = document.body.scrollWidth; // 페이지 전체 넓이
		var bodyheight = document.body.scrollHeight; // 페이지 전체 높이
		var y_max = 0; // iframe 안에 메인 페이지가 포함된 경우(ex. 네이버 블로그) puppeteer가 정상적으로 페이지의 높이를 가져오지 못해 노드들을 방문하며 높이를 갱신
		var tags = new Array(); // bottom line을 갱신하기 위해 tag, ccls, comments, posts 노드들을 저장
		var ccls = new Array();
		var comments = new Array();
		var posts = new Array();
		function getpos(node) { // 전체 페이지에 대한 노드의 좌표를 계산하기 위해 재귀 함수 사용
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
		function checkad(link){ // 링크가 다른 도메인 또는 머신에 연결되어 있는지 체크
			if(link == "#") return false;
			if(link[0] == "/") return false;
			let link_machine = link.split('.')[0].split('/')[2];
			let link_domain = link.split('.')[1];
			let url_machine = url.split('.')[0].split('/')[2];
			let url_domain = url.split('.')[1];
			if(link_domain != url_domain || link_machine != url_machine) return true;
			else return false;
		}

		function checkdiv(node){ // ad => return 0, 광고로 판단되는 노드를 div, p, span 단위로 제거
			let childnodes = node.childNodes;
			for(var i=0; i<childnodes.length; i++){
				if(["DIV", "P", "SPAN"].includes(childnodes[i].nodeName)) continue;
				if(childnodes[i].nodeName == "A"){
					let href = childnodes[i].getAttribute("href");
					if((href == "#" || /javascript/.test(href)==true && href.length < 20)==false) return 0;
				}
				if(checkdiv(childnodes[i]) == 0) return 0;
			}
			return 1;
		}

		function recur(root, indent, is_link, is_ad, framewidth, frameheight){ // 이 재귀 함수를 계속 돌면서 노드 정보를 저장함
			let contents = root.childNodes; // 현재 노드의 child들
			let result = new Array(); // result에 노드 정보들을 저장
			let attributes = new Array(); //(type, content, x, y, w, h, fontsize, bg_color, indent) : node의 attribute
			let childindent = indent;
			let isad = is_ad;
			for(var i=0; i<contents.length; i++){ // child를 모두 방문
				attributes = new Array(); // 노드들의 attribute를 저장
				let node = contents[i];
				let newframewidth = framewidth;
				let newframeheight = frameheight;
				if(["SCRIPT", "#comment", "STYLE", "NOSCRIPT"].includes(node.nodeName)) continue; // 페이지에 표시되지 않는 노드들 제거
				if(node.nodeValue != null){ // null인 경우는 이미지 또는 div 같은 노드
					if(node.nodeValue.trim().length != 0 && node.nodeName == "#text" && isad == false){ // 텍스트 노드 체크
						attributes.push("text"); // 노드 타입 저장
						attributes.push(node.nodeValue.trim()); // 노드의 내용 저장
						if(node.parentNode.innerHTML != node.nodeValue){ //태그가 없는 텍스트 노드의 경우는 <span> tag를 만들어 텍스트 노드에 감싸줌(tag가 없으면 텍스트 노드 자체의 좌표를 잡지 못함)
							let spantext = document.createTextNode(node.nodeValue);
							let insertspan = document.createElement('span');
							insertspan.appendChild(spantext);
							node.parentNode.insertBefore(insertspan, node);
							node.parentNode.removeChild(node);
							node = spantext;
							childindent += 1;
						}
						node = node.parentNode;
						let x = getpos(node).x + node.offsetWidth / 2 + framewidth; // 노드의 좌표 설정
						let y = getpos(node).y + node.clientTop + node.offsetHeight / 2 + frameheight;
						if(x <= 0 || y <= 0) continue; // 페이지에 표시되지 않는 경우
						attributes.push(x); // x좌표 저장
						attributes.push(y); // y좌표 저장
						let w = node.offsetWidth;
						let h = node.offsetHeight;
						if(w <= 1.0 || h <= 1.0) continue; // 페이지에 표시되지 않는 경우
						if(y + h/2 > y_max) y_max = y + h/2;
						attributes.push(w); // 넓이 저장
						attributes.push(h); // 높이 저장
						let size = window.getComputedStyle(node,null).getPropertyValue('font-size');
						size = size.split('p')[0]*1
						attributes.push(size); // 글씨크기 저장
						if(size <= 0) continue; // 페이지에 표시되지 않는 경우
						let bgcolor = window.getComputedStyle(node,null).getPropertyValue('background-color');
						attributes.push(bgcolor);
						attributes.push(childindent);
					}
				}
				else{
					if(window.getComputedStyle(node,null).getPropertyValue('display') == "none") continue; // 페이지에 표시되지 않는 경우
					let position = window.getComputedStyle(node,null).getPropertyValue('position');
					let z_index = window.getComputedStyle(node,null).getPropertyValue('z-index');
					if(node.nodeName == "IFRAME"){ // 현재 노드가 iframe인 경우 내부에 있는 body로 접근
						newframewidth = framewidth + getpos(node).x;
						newframeheight = frameheight + getpos(node).y;
						node = node.contentWindow.document.body;
						if(node == null){ // body가 없는 iframe의 경우 제외
							continue;
						}
					}
					else if(node.nodeName == "IMG"){ // 이미지 노드 체크
						if(isad == false){ // 광고로 판단되면 제외
							attributes.push("img"); // 노드 타입 저장
							attributes.push(node.src); // 이미지 url 저장
							let x = getpos(node).x + node.offsetWidth / 2 + framewidth;;
							let y = getpos(node).y + node.offsetHeight / 2 + frameheight;
							if(x <= 0 || y <= 0) continue;
							attributes.push(x); // x좌표 저장
							attributes.push(y); // y좌표 저장
							let w = node.offsetWidth;
							let h = node.offsetHeight;
							if(w <= 1 || h <= 1) continue;
							if(y + h/2 > y_max) y_max = y + h/2;
							attributes.push(w); // 넓이 저장
							attributes.push(h); // 높이 저장
							attributes.push(0); // 글씨크기는 0으로 저장
							attributes.push("rgba(0, 0, 0, 0)");
							attributes.push(childindent);
						}
					}
					if(node.childNodes != null && position != "fixed" && (z_index == "auto" || z_index < 10000)){ // <DIV>같이 내부에 child가 더 있는 노드의 경우(position과 z-index로 1차적으로 광고 판단)
						if(mode == 2){ // 블로그 카테고리
							let islink = is_link;
							if(node.nodeName == "A"){ // 다른 사이트로 링크가 연결된 <a> 태그 제거
								let href = node.getAttribute("href");
								if(href != "#") islink = true;
								if(href == null || checkad(href) == true) isad = true;
							}
							if(["DIV", "P", "SPAN", "DL"].includes(node.nodeName)){ 
								let is_skip = 0;
								node_class = node.getAttribute("class");
								node_id = node.getAttribute("id");
								let exp_bottom = [/tag/i,/ccl/i,/comment/i,/#post/i];
								let exp = [/category/i,/plugin/i,/player/i,/map/i];
								for(var j=0; j<exp_bottom.length; j++){ // 마지막에 bottom line을 계산하기 위해 해당하는 노드들을 저장
									if(exp_bottom[j].test(node_class) || exp_bottom[j].test(node_id)){
										is_skip = 1;
										let y = getpos(node).y + node.offsetHeight / 2 + frameheight;
										if(j == 0) tags.push(y);
										else if(j == 1) ccls.push(y);
										else if(j == 2) comments.push(y);
										else if(j == 3) posts.push(y);
										break;
									}
								}
								for(var j=0; j<exp.length; j++){ //category, plugin, player, map 제거
									if(exp[j].test(node_class) || exp[j].test(node_id)){
										is_skip = 1;
										break;
									}
								}
								if(is_skip == 1) continue;
							}
							result.push(recur(node,indent+1,islink,isad,newframewidth,newframeheight)); // 현재 노드를 root로 해서 재귀 함수를 다시 호출
							isad = is_ad;
						}
						else if(mode == 3){ // 쇼핑몰 카테고리
							if(["DIV", "P", "SPAN", "DL"].includes(node.nodeName) && checkdiv(node) == 0) continue;
							result.push(recur(node,indent+1,false,false,newframewidth,newframeheight)); // 현재 노드를 root로 해서 재귀 함수를 다시 호출
						}
						else{ // 뉴스 카테고리
							let islink = is_link;
							if(node.nodeName == "A"){
								let href = node.getAttribute("href");
								if(href != "#") islink = true;
								if(href == null || checkad(href) == true) isad = true;
							}
							result.push(recur(node,indent+1,islink,isad,newframewidth,newframeheight)); // 현재 노드를 root로 해서 재귀 함수를 다시 호출
							isad = is_ad;
						}
					}
				}
				result.push(attributes); // 저장했던 특징 값을 result에 저장
			}
			return result; // 재귀 함수의 return
		}
		body = document.querySelector("body");
		if(bodyheight <= 1000) return [recur(body,0,false,0,0,0), 1200, y_max, [tags,ccls,comments,posts]]; // iframe안에 메인 페이지가 들어 있는 경우(ex. 네이버 블로그) 페이지 전체 높이를 제대로 잡지 못해 y_max를 갱신하며 높이 측정
		return [recur(body,0,false,0,0,0), bodywidth, bodyheight, [tags,ccls,comments,posts]];
	}, url,mode);
	await browser.close();
	var bottoms = await nodes.pop(); // bottom line의 정보
	var bottom = await checkbottom(bottoms,nodes[nodes.length-1]); // bottom line을 계산
	await show(nodes,bottom); // stdout에 노드 정보들을 출력
	await process.stdout.write(""+nodes[nodes.length-2]+"\n"); // 페이지 전체 넓이
	await process.stdout.write(""+nodes[nodes.length-1]+"\n"); // 페이지 전체 높이
	await process.stdout.write(""+url+"\n"); // 페이지 url
}

 process.stdin.setEncoding("utf-8");
 process.stdout.setEncoding("utf-8");
 process.stdin.on('readable', () => { // 파이프연결로 python으로부터 url 정보를 받음
 	var url = process.stdin.read();
 	if(url){
 		parse(url);
 	}
 });