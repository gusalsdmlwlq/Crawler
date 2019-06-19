const puppeteer = require('puppeteer');

var node_list="";
const kafka = require('kafka-node');

let kafkaHost = 'kafka:9092';

const Consumer = kafka.Consumer;

const client = new kafka.KafkaClient({kafkaHost: kafkaHost});



const consumer = new Consumer(

    client,

    [

        { topic: 'url' },

    ],

    {

    groupId: 'console-consumer-53678',//consumer group id, default `kafka-node-group`
    // Auto commit config
    autoCommit: true,
    autoCommitIntervalMs: 5000,
    // The max wait time is the maximum amount of time in milliseconds to block waiting if insufficient data is available at the time the request is issued, default 100ms
    fetchMaxWaitMs: 100,
    // This is the minimum number of bytes of messages that must be available to give a response, default 1 byte
    fetchMinBytes: 1,
    // The maximum bytes to include in the message set for this partition. This helps bound the size of the response.
    fetchMaxBytes: 1024 * 1024,
    // If set true, consumer will fetch message from the given offset in the payloads
    fromOffset: false,
    // If set to 'buffer', values will be returned as raw buffer objects.
    encoding: 'utf8',
    keyEncoding: 'utf8'
    }

);



function add_list(a,b,c){
   node_list += a;
   node_list += b;
   node_list += c;
}
function send_data(data){

	Producer = kafka.Producer;
	let client = new kafka.KafkaClient({kafkaHost: kafkaHost});
	producer = new Producer(client),
	payloads = [
	{ 

			topic: 'node', 

			messages: data 

		}

	];



		client.on('ready', function (){

			console.log('client ready');

		})  



		client.on('error', function (err){

			console.log('client error: ' + err);

		})  



		producer.on('ready', function () {

			producer.send(payloads, function (err, data) {

				console.log('send: ' + data);        

				process.exit();

			});

		});



		producer.on('error', function (err) {

			console.log('error: ' + err);

			process.exit();

		});
}
function printarray(array,bottom){
   if(array[3]*1 > bottom) return;
   for(var i=0; i<array.length; i++){
      if(typeof(array[i]) == "string") node_list += (array[i].replace(/\n/gi, " ")+"\n");
      else node_list += (array[i]+"\n");
   }
}

function show(array,bottom){
   for(var i=0; i<array.length; i++){
      if(typeof(array[i]) == "string"){
         printarray(array,bottom);
         return;
      }
      else show(array[i],bottom);
   }
}

function checkbottom(bottoms,height){
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

async function parse(url_){
   var url = url_.split(" ")[0];
   var mode = url_.split(" ")[1];
   const browser = await puppeteer.launch({
       args: ["--no-sandbox", "--disable-web-security", "--user-data-dir=data", '--enable-features=NetworkService', '--start-fullscreen',  '--window-size=1920,1080']
   });
   const page = await browser.newPage();
   await page.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36");
   await page.goto(url);
   await page.waitFor(3000);
   const nodes = await page.evaluate((url,mode) => {
      var bodywidth = document.body.scrollWidth;
      var bodyheight = document.body.scrollHeight;
      var y_max = 0;
      var tags = new Array();
	  var ccls = new Array();
	  var comments = new Array();
	  var posts = new Array();
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
					if((href == "#" || /javascript/.test(href)==true && href.length < 20)==false) return 0;
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
                  if(is_link == false){
                     attributes.push("img");
                     attributes.push(node.src);
                     let x = getpos(node).x + node.offsetWidth / 2 + framewidth;;
                     let y = getpos(node).y + node.offsetHeight / 2 + frameheight;
                     if(x <= 0 || y <= 0) continue;
                     attributes.push(x);
                     attributes.push(y);
                     let w = node.offsetWidth;
                     let h = node.offsetHeight;
                     if(w <= 1 || h <= 1) continue;
                     if(y + h/2 > y_max) y_max = y + h/2;
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
                    if(["DIV", "P", "SPAN", "DL"].includes(node.nodeName)){ 
                      let is_skip = 0;
                      node_class = node.getAttribute("class");
                      node_id = node.getAttribute("id");
                      let exp_bottom = [/tag/i,/ccl/i,/comment/i,/#post/i];
                      let exp = [/category/i,/plugin/i,/player/i,/map/i];
                      for(var j=0; j<exp_bottom.length; j++){ //bottom 갱신
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
                    if(["DIV", "P", "SPAN", "DL"].includes(node.nodeName) && checkdiv(node) == 0) continue;
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
      if(bodyheight <= 1000) return [recur(body,0,false,0,0,0), 1200, y_max, [tags,ccls,comments,posts]];
      return [recur(body,0,false,0,0,0), bodywidth, bodyheight, [tags,ccls,comments,posts]];
   }, url, mode);
   await browser.close();
   var bottoms = await nodes.pop();
   var bottom = await checkbottom(bottoms,nodes[nodes.length-1]);
   await show(nodes,bottom);
   await add_list(""+nodes[nodes.length-2]+"\n", ""+nodes[nodes.length-1]+"\n", ""+url+"\n");
   await send_data(node_list);
}


consumer.on('message', function (message) {

    var url =message.value;
	if(url){
      parse(url);
   }

});
consumer.on('error', function (err) {

    console.log('Error:',err);

});



consumer.on('offsetOutOfRange', function (err) {

    console.log('offsetOutOfRange:',err);

});