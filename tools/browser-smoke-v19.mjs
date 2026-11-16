import { chromium } from 'playwright';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const inputs=process.argv.slice(2);
const browser=await chromium.launch({headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--enable-unsafe-swiftshader']});
let results=[];
for(const input of inputs){
 const page=await browser.newPage({viewport:{width:1280,height:800}});
 const errors=[];
 page.on('pageerror',e=>errors.push('PAGEERROR: '+String(e.stack||e.message).slice(0,4500)));
 page.on('console',msg=>{if(msg.type()==='error')errors.push('CONSOLE: '+msg.text().slice(0,1500))});
 try{
 await page.goto(pathToFileURL(path.resolve(input)).href,{waitUntil:'domcontentloaded',timeout:20000});
 await page.waitForTimeout(4000);
 const state=await page.evaluate(()=>{
 const buttons=document.querySelectorAll('#filterButtons button');
 return {buttons:buttons.length,status:document.getElementById('status')?.textContent,err:document.getElementById('err')?.textContent,mapCanvas:!!document.getElementById('gl'),geoCanvas:!!document.getElementById('poiCanvas'),footer:document.querySelector('#filters')?.getBoundingClientRect()?.height,webgl2:!!document.createElement('canvas').getContext('webgl2')};
 });
 results.push({input,state,errors});
 }catch(e){results.push({input,error:String(e),errors})}
 await page.close();
}
await browser.close();
console.log(JSON.stringify(results,null,2));
