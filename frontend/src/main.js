import './style.css'

const services = [
{id:1,icon:"palette",color:"#A78BFA",title:"التصميم الجرافيكي",desc:"تصميم الشعارات، الهويات البصرية، البنرات، الإعلانات، والمطبوعات بأعلى جودة إبداعية.",
 short:"تصميم جرافيك احترافي",imgs:["design-1","design-2","design-3","design-4","design-5"],
 features:["تصميم الشعارات والهويات البصرية","تصميم البنرات والإعلانات المطبوعة","تصميم المطبوعات التجارية (كروت، بروشورات)","تصميم واجهات ومواقع إلكترونية","معالجة الصور وتحسينها احترافياً","تصميم محتوى السوشيال ميديا"],
 detail:"نقدم خدمات التصميم الجرافيكي المتكاملة التي تجعل علامتك التجارية مميزة. من الشعارات إلى الهويات البصرية المتكاملة، ومن تصاميم السوشيال ميديا إلى المطبوعات الاحترافية — كل ما تحتاجه لهوية بصرية قوية ومؤثرة."},
{id:2,icon:"video",color:"#F59E0B",title:"مونتاج الفيديو",desc:"مونتاج احترافي، موشن جرافيك، أنيميشن، وفيديوهات دعائية لعلامتك التجارية.",
 short:"فيديو احترافي بإبداع",imgs:["video-1","video-2","video-3","video-4"],
 features:["مونتاج فيديو احترافي","موشن جرافيك ثنائي وثلاثي الأبعاد","رسوم متحركة وأنيميشن","فيديوهات دعائية وإعلانية","مونتاج أفلام قصيرة وفيديوهات توعوية","تصحيح ألوان ومؤثرات بصرية"],
 detail:"فريقنا المتخصص في المونتاج يقدم لك فيديوهات احترافية تنقل رسالتك بأفضل صورة. باستخدام أحدث البرامج والتقنيات، نضمن لك محتوى فيديو جذاب يلفت انتباه جمهورك ويحقق أهدافك التسويقية."},
{id:3,icon:"chart-line",color:"#A78BFA",title:"إدارة السوشيال ميديا",desc:"إدارة حساباتك، إنشاء المحتوى، جدولة المنشورات، وزيادة التفاعل والمتابعين.",
 short:"نمو متواصل على السوشيال",imgs:["social-1","social-2","social-3","social-4"],
 features:["إدارة حسابات التواصل الاجتماعي","إنشاء وتصميم المحتوى اليومي","جدولة المنشورات وإدارة التقويم","زيادة التفاعل والمتابعين العضويين","تحليل الأداء وتقارير شهرية","استراتيجيات تسويق مخصصة"],
 detail:"نأخذ حساباتك على وسائل التواصل الاجتماعي إلى مستوى جديد. خطط محتوى مخصصة، تصاميم جذابة، وجدولة منتظمة — كل ذلك لضمان نمو متواصل وتفاعل حقيقي مع جمهورك المستهدف."},
{id:4,icon:"bullhorn",color:"#F59E0B",title:"التسويق الرقمي",desc:"حملات إعلانية مدفوعة، تحسين محركات البحث، واستراتيجيات تسويق متكاملة.",
 short:"حملات تسويق تحقق نتائج",imgs:["marketing-1","marketing-2"],
 features:["حملات إعلانية ممولة (Facebook/Google)","تحسين محركات البحث (SEO)","استراتيجيات تسويق متكاملة","تحليل السوق والمنافسين","إعادة استهداف الزوار","تقارير أداء وROI"],
 detail:"نصمم وننفذ حملات تسويق رقمي تحقق أعلى عائد استثمار. فريقنا المتخصص في الإعلانات الممولة وتحسين محركات البحث يضمن ظهورك أمام الجمهور المناسب في الوقت المناسب."},
{id:5,icon:"ad",color:"#A78BFA",title:"الدعاية والإعلان",desc:"تصميم وإنتاج محتوى دعائي وإعلاني للمطبوعات، اللوحات، والمنصات الرقمية.",
 short:"إعلانات لا تُنسى",imgs:["ads-1","ads-2","ads-3","ads-4"],
 features:["تصميم إعلانات مطبوعة ورقمية","لوحات إعلانية خارجية","إعلانات صحف ومجلات","إعلانات منصات التواصل","تصميم بروشورات وكتيبات دعائية","حملات إعلانية متكاملة"],
 detail:"من تصميم الإعلان المطبوع إلى اللوحات الإعلانية الرقمية — نقدم حلول دعاية وإعلان متكاملة تجعل علامتك التجارية في مقدمة المشهد. إبداع في التصميم ودقة في التنفيذ."},
{id:6,icon:"print",color:"#F59E0B",title:"الطباعة الديجيتال والأوفسيت",desc:"طباعة ديجيتال وأوفسيت بجودة عالية للبروشورات، الكروت، البنرات، الكتب، والمجلات.",
 short:"طباعة فاخرة بجودة عالية",imgs:["print-1","print-2","print-3","print-4"],
 features:["طباعة ديجيتال عالية الجودة","طباعة أوفسيت للكميات الكبيرة","طباعة البنرات واللوحات","طباعة الكتب والمجلات","طباعة الكروت الشخصية والأظرف","تغليف وتجليد فاخر"],
 detail:"أحدث ماكينات الطباعة الديجيتال والأوفسيت مع فريق فني متخصص يضمن لك أفضل جودة طباعة. نقدم خدمات طباعة متكاملة من أصغر الكميات إلى أكبر الإنتاجات بأسعار تنافسية."}
]

const marketingSolutions = [
{id:1,icon:"copyright",iconType:"far",color:"#F32020",title:"Branding",desc:"Branding packages are affordable and effective marketing kits that provide you with the items necessary to help your business stand out.",
 imgs:["branding-1","branding-2","branding-3","branding-4"],
 features:["Brand identity & logo design","Business card & stationery design","Brand guidelines book","Packaging design","Brand strategy consulting","Visual identity system"],
 detail:"Our comprehensive branding packages give your business a cohesive, memorable identity that stands out in the market. From logo design to full brand guidelines, we ensure consistency across every touchpoint."},
{id:2,icon:"map-signs",iconType:"fas",color:"#20F346",title:"Outdoor Advertising",desc:"Since consumers spend more time out of their homes then in them, outdoor advertising is highly effective.",
 imgs:["outdoor-1","outdoor-2","outdoor-3","outdoor-4"],
 features:["Billboard & banner design","Street furniture advertising","Transit & vehicle ads","Digital out-of-home (DOOH)","Large format printing","Placement strategy & planning"],
 detail:"Reach your audience where they live, work, and travel. Our outdoor advertising solutions combine creative design with strategic placement to maximize visibility and impact for your brand."},
{id:3,icon:"paint-brush",iconType:"fas",color:"#F320E3",title:"Design House GFX",desc:"Creative design solutions for your brand — from concept to execution, we bring your visual identity to life.",
 imgs:["gfx-1","gfx-2","gfx-3","gfx-4"],
 features:["Creative graphic design","Photo retouching & enhancement","3D modeling & rendering","Infographic design","Presentation design","Motion graphics"],
 detail:"Our design house is a creative powerhouse delivering stunning visuals across all media."},
{id:4,icon:"shopping-cart",iconType:"fas",color:"#2063F3",title:"E-Commerce System",desc:"Build and scale your online store with our comprehensive e-commerce solutions tailored to your business needs.",
 imgs:["ecommerce-1","ecommerce-2","ecommerce-3","ecommerce-4"],
 features:["Online store setup & design","Product catalog management","Payment gateway integration","Shipping & logistics setup","SEO for e-commerce","Performance analytics"],
 detail:"Launch and scale your online store with our end-to-end e-commerce solutions."},
{id:5,icon:"globe",iconType:"fas",color:"#A3F320",title:"Web Services",desc:"From web design to development, we provide end-to-end web services that establish your brand online presence.",
 imgs:["web-1","web-2","web-3","web-4"],
 features:["Website design & development","Responsive & mobile-first design","CMS integration (WordPress etc.)","Landing page creation","Website maintenance & support","Performance optimization"],
 detail:"Establish a powerful online presence with our professional web services."},
{id:6,icon:"tools",iconType:"fas",color:"#F3A020",title:"Marketing Tools",desc:"Power your campaigns with professional marketing tools and analytics to track, measure, and optimize your ROI.",
 imgs:["mtools-1","mtools-2","mtools-3","mtools-4"],
 features:["Marketing automation setup","Analytics & tracking dashboards","CRM integration","Email marketing campaigns","A/B testing tools","ROI reporting & insights"],
 detail:"Empower your marketing with the right tools and analytics."},
{id:7,icon:"share-alt",iconType:"fas",color:"#E320F3",title:"Social Presence & Campaign",desc:"Build a strong social media presence with targeted campaigns that engage your audience and drive real results.",
 imgs:["social-m-1","social-m-2","social-m-3","social-m-4"],
 features:["Social media strategy development","Content creation & curation","Influencer marketing campaigns","Social media advertising","Community management","Performance tracking & reporting"],
 detail:"Build a commanding social media presence with targeted campaigns."},
{id:8,icon:"server",iconType:"fas",color:"#20F3C3",title:"Domain & Hosting",desc:"Reliable domain registration and web hosting services to keep your website secure, fast, and always online.",
 imgs:["hosting-1","hosting-2","hosting-3","hosting-4"],
 features:["Domain registration & transfer","Shared & VPS hosting","SSL certificate setup","Email hosting","CDN integration","24/7 technical support"],
 detail:"Reliable domain registration and hosting services."}
]

const portfolios = [
{id:1,title:"الهوية البصرية — تكافل",cat:"design",catAr:"تصميم",client:"شركة تكافل للتأمين",desc:"هوية بصرية متكاملة",img:"design-1"},
{id:2,title:"حملة إعلانية — مذاق",cat:"design",catAr:"تصميم",client:"مطعم مذاق",desc:"تصاميم إعلانية لموسم رمضان",img:"design-2"},
{id:3,title:"تصميم متجر إلكتروني",cat:"design",catAr:"تصميم",client:"متجر أزياء",desc:"تصميم واجهة متجر بهوية بصرية",img:"design-3"},
{id:4,title:"هوية بصرية — شركة ناشئة",cat:"design",catAr:"تصميم",client:"شركة تقنية",desc:"هوية بصرية كاملة",img:"design-4"},
{id:5,title:"بوسترات حملة إعلانية",cat:"design",catAr:"تصميم",client:"متجر مجوهرات",desc:"تصميم صور منتجات وبنرات",img:"design-5"},
{id:6,title:"فيديو افتتاحي — المنارة",cat:"video",catAr:"فيديو",client:"شركة المنارة العقارية",desc:"فيديو افتتاحي بمونتاج احترافي",img:"video-1"},
{id:7,title:"سلسلة فيديوهات توعوية",cat:"video",catAr:"فيديو",client:"منظمة بصيرة",desc:"10 فيديوهات توعوية",img:"video-2"},
{id:8,title:"إعلان متحرك — منتج جديد",cat:"video",catAr:"فيديو",client:"شركة تقنية",desc:"إعلان متحرك 30 ثانية",img:"video-3"},
{id:9,title:"فيديو موشن — منتج غذائي",cat:"video",catAr:"فيديو",client:"شركة أغذية",desc:"فيديو موشن جرافيك 45 ثانية",img:"video-4"},
{id:10,title:"إدارة حسابات — متجر أزياء",cat:"social",catAr:"سوشيال",client:"متجر إلكتروني",desc:"إدارة كاملة +250% متابعين",img:"social-1"},
{id:11,title:"حملة تسويقية — مهرجان",cat:"social",catAr:"سوشيال",client:"مهرجان ثقافي",desc:"حملة تسويق عبر منصات التواصل",img:"social-2"},
{id:12,title:"إطلاق علامة تجارية",cat:"social",catAr:"سوشيال",client:"علامة تجارية",desc:"استراتيجية إطلاق متكاملة",img:"social-3"},
{id:13,title:"حملة موسمية — فندق",cat:"social",catAr:"سوشيال",client:"فندق سياحي",desc:"حملة سوشيال مédia للموسم الصيفي",img:"social-4"},
{id:14,title:"حملة إعلانات ممولة",cat:"marketing",catAr:"تسويق",client:"شركة عقارات",desc:"حملة ممولة حققت ROI 400%",img:"marketing-1"},
{id:15,title:"تحسين محركات البحث",cat:"marketing",catAr:"تسويق",client:"متجر أونلاين",desc:"ظهور في الصفحة الأولى",img:"marketing-2"},
{id:16,title:"تصميم إعلان — صحيفة",cat:"ads",catAr:"دعاية",client:"شركة سيارات",desc:"إعلان صحفي كامل الصفحة",img:"ads-1"},
{id:17,title:"لوحات إعلانية رقمية",cat:"ads",catAr:"دعاية",client:"شركة اتصالات",desc:"تصاميم لوحات إعلانية رقمية",img:"ads-2"},
{id:18,title:"حملة إعلانية متكاملة",cat:"ads",catAr:"دعاية",client:"مطعم",desc:"حملة تشمل مطبوعات ولوحات",img:"ads-3"},
{id:19,title:"إعلان — مركز تجاري",cat:"ads",catAr:"دعاية",client:"مركز تجاري",desc:"تصميم وطباعة إعلانات",img:"ads-4"},
{id:20,title:"كتيب شركة — بروشور",cat:"print",catAr:"طباعة",client:"شركة استشارات",desc:"تصميم وطباعة كتيب بروشور",img:"print-1"},
{id:21,title:"هوية مطبوعة — كروت",cat:"print",catAr:"طباعة",client:"بنك",desc:"تصميم وطباعة كروت شخصية",img:"print-2"},
{id:22,title:"كتاب فني — مجلد",cat:"print",catAr:"طباعة",client:"دار نشر",desc:"إخراج وطباعة كتاب فني",img:"print-3"},
{id:23,title:"طباعة أوفسيت — مجلة",cat:"print",catAr:"طباعة",client:"مجلة شهرية",desc:"طباعة 64 صفحة بكمية 10000",img:"print-4"}
]

const categories = [
{key:"all",label:"الكل"},{key:"design",label:"تصميم"},{key:"video",label:"فيديو"},
{key:"social",label:"سوشيال"},{key:"marketing",label:"تسويق"},{key:"ads",label:"دعاية"},{key:"print",label:"طباعة"}
]

const giveaways = [
{id:1,title:"مسابقة رمضان 2026",desc:"شارك واربح 5000 ج.م نقداً!",img:"giveaway-1",prize:"5000 ج.م",winners:3},
{id:2,title:"مسابقة التصميم الأفضل",desc:"أفضل تصميم جرافيك يفوز باشتراك Canva Pro",img:"giveaway-2",prize:"اشتراك Canva Pro",winners:1},
{id:3,title:"جائزة العميل الشهري",desc:"خصم 50% على الخدمة القادمة",img:"giveaway-3",prize:"خصم 50%",winners:1},
{id:4,title:"مسابقة الفيديو التفاعلي",desc:"أفضل فيديو تفاعلي يفوز بـ 3000 ج.م",img:"giveaway-4",prize:"3000 ج.م",winners:2},
{id:5,title:"جائزة الإحالة",desc:"كل عميل يحيل صديق يحصل على جلسة تصميم مجانية",img:"giveaway-5",prize:"جلسة تصميم",winners:5},
{id:6,title:"مسابقة الهوية البصرية",desc:"قدم هويتك واربح طباعة كاملة مجاناً",img:"giveaway-6",prize:"طباعة مجانية",winners:2},
{id:7,title:"عيد الأضحى — جائزة كبرى",desc:"بطاقة شرائية بقيمة 10000 ج.م",img:"giveaway-7",prize:"10000 ج.م",winners:1},
{id:8,title:"مسابقة المتابعين",desc:"تفاعل معنا واربح اشتراكات في خدماتنا",img:"giveaway-8",prize:"خدمات شهر",winners:3}
]

// ─── Custom Cursor ───
const cursorDot=document.createElement('div');cursorDot.className='cursor-dot';document.body.appendChild(cursorDot);
const cursorRing=document.createElement('div');cursorRing.className='cursor-ring';document.body.appendChild(cursorRing);
let mouseX=0,mouseY=0,ringX=0,ringY=0;
document.addEventListener('mousemove',e=>{
  mouseX=e.clientX;mouseY=e.clientY;
  cursorDot.style.left=mouseX+'px';cursorDot.style.top=mouseY+'px';
});
function animateRing(){ringX+=(mouseX-ringX)*0.12;ringY+=(mouseY-ringY)*0.12;cursorRing.style.left=ringX+'px';cursorRing.style.top=ringY+'px';requestAnimationFrame(animateRing)}
animateRing();
document.querySelectorAll('a,button,.btn,.service-card,.portfolio-item,.giveaway-card,.filter-btn,.hero-stat').forEach(el=>{
  el.addEventListener('mouseenter',()=>{cursorRing.classList.add('hover');cursorDot.classList.add('hover')});
  el.addEventListener('mouseleave',()=>{cursorRing.classList.remove('hover');cursorDot.classList.remove('hover')})
});
document.addEventListener('mouseleave',()=>{cursorDot.style.opacity='0';cursorRing.style.opacity='0'});
document.addEventListener('mouseenter',()=>{cursorDot.style.opacity='1';cursorRing.style.opacity='1'});

const glowDot=document.createElement('div');glowDot.className='mouse-glow';document.body.appendChild(glowDot);
document.addEventListener('mousemove',e=>{glowDot.style.left=e.clientX+'px';glowDot.style.top=e.clientY+'px';glowDot.classList.add('visible')});
document.addEventListener('mouseleave',()=>glowDot.classList.remove('visible'));

// ─── Scroll Progress ───
const scrollProgress=document.createElement('div');scrollProgress.className='scroll-progress';document.body.prepend(scrollProgress);
window.addEventListener('scroll',()=>{const h=document.documentElement;const p=(h.scrollTop/(h.scrollHeight-h.clientHeight))*100;scrollProgress.style.width=p+'%'});

// ─── Magnetic Buttons ───
document.querySelectorAll('.btn-primary,.btn-whatsapp,.btn-phone,.nav-cta').forEach(btn=>{
  const wrap=document.createElement('span');wrap.className='magnetic-wrap';
  btn.parentNode.insertBefore(wrap,btn);wrap.appendChild(btn);
  wrap.addEventListener('mousemove',e=>{
    const r=wrap.getBoundingClientRect();
    const x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;
    btn.style.transform=`translate(${x*0.2}px,${y*0.2}px)`
  });
  wrap.addEventListener('mouseleave',()=>{btn.style.transform=''})
});

const canvas=document.getElementById('particles-canvas'),ctx=canvas.getContext('2d');
let particles=[],mouse={x:null,y:null};
function resizeCanvas(){canvas.width=window.innerWidth;canvas.height=window.innerHeight}
resizeCanvas();window.addEventListener('resize',resizeCanvas);

const COLORS=['rgba(167,139,250','rgba(245,158,11','rgba(236,72,153','rgba(52,211,153'];
class Particle{
constructor(){this.reset()}
reset(){
this.x=Math.random()*canvas.width;this.y=Math.random()*canvas.height;
this.size=Math.random()*3+0.5;this.vx=(Math.random()-0.5)*0.6;this.vy=(Math.random()-0.5)*0.6;
this.opacity=Math.random()*0.5+0.15;this.color=COLORS[Math.floor(Math.random()*COLORS.length)];
this.pulseSpeed=Math.random()*0.02+0.005;this.pulseOffset=Math.random()*Math.PI*2;
this.isStar=Math.random()>0.85
}
update(){
this.x+=this.vx;this.y+=this.vy;
if(this.x<0||this.x>canvas.width||this.y<0||this.y>canvas.height)this.reset();
const dx=mouse.x?mouse.x-this.x:0,dy=mouse.y?mouse.y-this.y:0;
const dist=Math.sqrt(dx*dx+dy*dy);
if(dist<150){const force=(1-dist/150)*0.005;this.vx-=dx*force;this.vy-=dy*force}
this.vx*=0.98;this.vy*=0.98
}
draw(){
const pulse=Math.sin(Date.now()*this.pulseSpeed+this.pulseOffset)*0.3+0.7;
const o=this.opacity*pulse;
if(this.isStar){
ctx.save();ctx.translate(this.x,this.y);
const spikes=4,outerR=this.size*2,innerR=this.size*0.8;
ctx.beginPath();
for(let i=0;i<spikes*2;i++){
const r=i%2===0?outerR:innerR;
const angle=i*Math.PI/spikes-Math.PI/2;
i===0?ctx.moveTo(r*Math.cos(angle),r*Math.sin(angle)):ctx.lineTo(r*Math.cos(angle),r*Math.sin(angle))
}ctx.closePath();
ctx.fillStyle=`${this.color},${o*0.8})`;ctx.fill();
ctx.restore()
}else{
ctx.beginPath();ctx.arc(this.x,this.y,this.size*pulse,0,Math.PI*2);
ctx.fillStyle=`${this.color},${o})`;ctx.fill()
}
}
}

for(let i=0;i<120;i++)particles.push(new Particle);

function animateParticles(){
ctx.clearRect(0,0,canvas.width,canvas.height);
particles.forEach(p=>{p.update();p.draw()});
for(let i=0;i<particles.length;i++){
for(let j=i+1;j<particles.length;j++){
const dx=particles[i].x-particles[j].x,dy=particles[i].y-particles[j].y;
const dist=Math.sqrt(dx*dx+dy*dy);
if(dist<180){
const alpha=0.06*(1-dist/180);
ctx.beginPath();ctx.moveTo(particles[i].x,particles[i].y);
ctx.lineTo(particles[j].x,particles[j].y);
ctx.strokeStyle=`rgba(167,139,250,${alpha})`;ctx.stroke()
}
}
}
requestAnimationFrame(animateParticles)
}
animateParticles();
document.addEventListener('mousemove',e=>{mouse.x=e.clientX;mouse.y=e.clientY});

const phrases=['تصميم جرافيك إبداعي','مونتاج فيديو احترافي','إدارة سوشيال ميديا','دعاية وإعلان','طباعة ديجيتال وأوفسيت','حلول تسويق متكاملة'];
let phraseIdx=0,charIdx=0,isDeleting=false;
function typewriter(){
const el=document.getElementById('typewriterText');
const current=phrases[phraseIdx];
if(isDeleting){charIdx--;el.textContent=current.substring(0,charIdx)}
else{charIdx++;el.textContent=current.substring(0,charIdx)}
if(!isDeleting&&charIdx===current.length){isDeleting=true;setTimeout(typewriter,2000);return}
if(isDeleting&&charIdx===0){isDeleting=false;phraseIdx=(phraseIdx+1)%phrases.length}
setTimeout(typewriter,isDeleting?40:80)
}
typewriter();

function animateCounters(){
document.querySelectorAll('.counter').forEach(el=>{
const target=parseInt(el.dataset.target);
const duration=1500;const start=performance.now();
function update(now){
const elapsed=now-start;const progress=Math.min(elapsed/duration,1);
const eased=1-Math.pow(1-progress,3);
const current=Math.round(eased*target);
el.textContent=current;
if(progress<1)requestAnimationFrame(update)
}
el.textContent=0;requestAnimationFrame(update)
})}

const heroCard=document.getElementById('heroCard');
if(heroCard){
heroCard.addEventListener('mousemove',e=>{
const rect=heroCard.getBoundingClientRect();
const x=(e.clientX-rect.left)/rect.width-0.5,y=(e.clientY-rect.top)/rect.height-0.5;
heroCard.style.transform=`rotateY(${x*10}deg) rotateX(${-y*10}deg)`
});
heroCard.addEventListener('mouseleave',()=>{heroCard.style.transform='rotateY(0deg) rotateX(0deg)'})
}
document.querySelectorAll('.service-card, .giveaway-card').forEach(card=>{
card.addEventListener('mousemove',e=>{
const r=card.getBoundingClientRect();
const x=(e.clientX-r.left)/r.width-0.5,y=(e.clientY-r.top)/r.height-0.5;
card.style.transform=`perspective(800px) rotateY(${x*5}deg) rotateX(${-y*5}deg) translateY(-4px)`
});
card.addEventListener('mouseleave',()=>{card.style.transform=''})
});

function renderServices(){
const container=document.getElementById('servicesContainer');
container.innerHTML=services.map((s,i)=>`
<div class="service-card reveal reveal-delay-${i}" onclick="openServiceModal(${s.id})" style="cursor:pointer">
<div class="shimmer"></div>
<div class="service-icon" style="color:${s.color}"><i class="fas fa-${s.icon}"></i></div>
<h3>${s.title}</h3><p>${s.desc}</p>
</div>`).join('')
}

function renderMarketing(){
const container=document.getElementById('marketingGrid');
container.innerHTML=marketingSolutions.map((m,i)=>`
<div class="service-card reveal reveal-delay-${i%4}" onclick="openMarketingModal(${m.id})" style="cursor:pointer">
<div class="shimmer"></div>
<div class="service-icon" style="color:${m.color}"><i class="${m.iconType} fa-${m.icon}"></i></div>
<h3>${m.title}</h3><p>${m.desc}</p>
</div>`).join('')
}
window.openMarketingModal=function(id){
const m=marketingSolutions.find(s=>s.id===id);
if(!m)return;
const modal=document.getElementById('marketingModal');
document.getElementById('mModalIcon').innerHTML=`<i class="${m.iconType} fa-${m.icon}" style="color:${m.color}"></i>`;
document.getElementById('mModalIcon').style.borderColor=m.color+'33';
document.getElementById('mModalTitle').textContent=m.title;
document.getElementById('mModalDesc').textContent=m.desc;
document.getElementById('mModalDetail').textContent=m.detail;
document.getElementById('mModalGallery').innerHTML=(m.imgs||[]).map(img=>
`<img src="images/${img}.jpg" alt="" loading="lazy" onclick="window.open('images/${img}.jpg','_blank')" onerror="this.style.display='none'" style="width:100%;height:160px;object-fit:cover;border-radius:12px;border:1px solid var(--border);cursor:pointer;transition:0.3s">`
).join('');
document.getElementById('mModalFeatures').innerHTML=m.features.map(f=>
`<div class="service-modal-feature"><i class="fas fa-check-circle"></i> ${f}</div>`
).join('');
modal.classList.add('open');
document.body.style.overflow='hidden'
}
window.closeMarketingModal=function(){
document.getElementById('marketingModal').classList.remove('open');
document.body.style.overflow=''
}
document.getElementById('marketingModal')?.addEventListener('click',function(e){
if(e.target===this)closeMarketingModal()
});

window.openServiceModal=function(id){
const s=services.find(s=>s.id===id);
if(!s)return;
const modal=document.getElementById('serviceModal');
document.getElementById('sModalIcon').innerHTML=`<i class="fas fa-${s.icon}" style="color:${s.color}"></i>`;
document.getElementById('sModalIcon').style.borderColor=s.color+'33';
document.getElementById('sModalTitle').textContent=s.title;
document.getElementById('sModalShort').textContent=s.short;
document.getElementById('sModalDetail').textContent=s.detail;
document.getElementById('sModalGallery').innerHTML=s.imgs.map(img=>
`<img src="images/${img}.jpg" alt="" loading="lazy" onclick="window.open('images/${img}.jpg','_blank')" onerror="this.style.display='none'">`
).join('');
document.getElementById('sModalFeatures').innerHTML=s.features.map(f=>
`<div class="service-modal-feature"><i class="fas fa-check-circle"></i> ${f}</div>`
).join('');
modal.classList.add('open');
document.body.style.overflow='hidden'
}
window.closeServiceModal=function(){
document.getElementById('serviceModal').classList.remove('open');
document.body.style.overflow=''
}
document.getElementById('serviceModal')?.addEventListener('click',function(e){
if(e.target===this)closeServiceModal()
});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeServiceModal()});

let currentFilter='all';
function renderPortfolio(filter='all'){
currentFilter=filter;
const grid=document.getElementById('portfolioGrid');
const items=filter==='all'?portfolios:portfolios.filter(p=>p.cat===filter);
grid.innerHTML=items.map((p,i)=>`
<div class="portfolio-item reveal reveal-delay-${i%4}" data-cat="${p.cat}" onclick="openLightbox(${p.id})">
<img src="images/${p.img}.jpg" alt="${p.title}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=\\'placeholder\\'><i class=\\'fas fa-image\\'></i><span>${p.title}</span></div>'">
<div class="portfolio-overlay">
<span class="cat-badge">${p.catAr}</span>
<h4>${p.title}</h4><p>${p.client}</p>
</div>
</div>`).join('');
renderFilters();
setTimeout(observeReveal,100)
}
window.filterPortfolio=function(cat){
document.querySelectorAll('.filter-btn').forEach(b=>b.classList.toggle('active',b.getAttribute('onclick')===`filterPortfolio('${cat}')`));
renderPortfolio(cat)
}

function renderFilters(){
const container=document.getElementById('portfolioFilters');
container.innerHTML=categories.map(c=>`<button class="filter-btn ${c.key==='all'?'active':''}" onclick="filterPortfolio('${c.key}')">${c.label}</button>`).join('')
}

let lightboxIdx=0;
window.openLightbox=function(id){
const items=currentFilter==='all'?portfolios:portfolios.filter(p=>p.cat===currentFilter);
lightboxIdx=items.findIndex(p=>p.id===id);
if(lightboxIdx===-1)return;
const p=items[lightboxIdx];
document.getElementById('lightboxImg').src=`images/${p.img}.jpg`;
document.getElementById('lightboxTitle').textContent=p.title;
document.getElementById('lightboxDesc').textContent=`${p.client} — ${p.desc}`;
document.getElementById('lightbox').classList.add('open');
document.body.style.overflow='hidden'
}
window.closeLightbox=function(){
document.getElementById('lightbox').classList.remove('open');
document.body.style.overflow=''
}
window.navigateLightbox=function(dir){
const items=currentFilter==='all'?portfolios:portfolios.filter(p=>p.cat===currentFilter);
lightboxIdx=(lightboxIdx+dir+items.length)%items.length;
const p=items[lightboxIdx];
document.getElementById('lightboxImg').src=`images/${p.img}.jpg`;
document.getElementById('lightboxTitle').textContent=p.title;
document.getElementById('lightboxDesc').textContent=`${p.client} — ${p.desc}`
}
document.addEventListener('keydown',e=>{
if(e.key==='Escape')closeLightbox();
if(e.key==='ArrowRight')navigateLightbox(-1);
if(e.key==='ArrowLeft')navigateLightbox(1)
});

function renderGiveaway(){
const container=document.getElementById('giveawayGrid');
container.innerHTML=giveaways.map((g,i)=>`
<div class="giveaway-card reveal reveal-delay-${i%4}">
<img src="images/${g.img}.jpg" alt="${g.title}" loading="lazy" onerror="this.style.display='none'">
<div class="giveaway-card-body">
<h3>${g.title}</h3>
<p>${g.desc}</p>
<span class="giveaway-tag"><i class="fas fa-trophy"></i> ${g.prize}</span>
<span class="giveaway-tag prize"><i class="fas fa-users"></i> ${g.winners} فائزين</span>
</div>
</div>`).join('')
}

async function handleQuoteSubmit(e){
e.preventDefault();
const btn=e.target.querySelector('button[type="submit"]');
const status=document.getElementById('quoteStatus');
btn.disabled=true;btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> جاري الإرسال...';
status.className='form-status';status.style.display='none';
const data={
name:document.getElementById('qName').value.trim(),
email:document.getElementById('qEmail').value.trim(),
phone:document.getElementById('qPhone').value.trim(),
service:document.getElementById('qService').value,
details:document.getElementById('qDetails').value.trim()
};
try{
const res=await fetch('/api/quotes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
const result=await res.json();
if(res.ok){
status.className='form-status success';
status.textContent='✅ تم إرسال الطلب! سنتواصل معك خلال 24 ساعة.';
window.open(`https://wa.me/201002711494?text=${encodeURIComponent(`طلب عرض سعر جديد 🚀
العميل: ${data.name}
الهاتف: ${data.phone}
الخدمة: ${data.service}
التفاصيل: ${data.details}
— أرسل من موقع Zain Media`)}`,'_blank');
const custPhone=data.phone.replace(/[^0-9]/g,'');
if(custPhone){
const waNum=custPhone.startsWith('0')?'20'+custPhone.slice(1):custPhone.startsWith('0020')?'20'+custPhone.slice(3):custPhone.startsWith('+')?custPhone.slice(1):custPhone;
window.open(`https://wa.me/${waNum}?text=${encodeURIComponent(`شكراً لتواصلك مع Zain Media 🎉

أهلاً ${data.name}،

تم استلام طلب عرض السعر الخاص بك للخدمة: ${data.service}

سيتم التواصل معكم عن طريق فريق متخصص لدينا في أقرب وقت ممكن خلال 24 ساعة.

📞 واتساب: +20 100 271 1494
📞 اتصال: +20 100 271 1494 / +20 112 226 5251
🌐 Zain Media`)}`,'_blank');
}
e.target.reset()
}else{throw new Error(result.error||'حدث خطأ')}
}catch(err){
status.className='form-status error';
status.textContent='❌ '+err.message
}status.style.display='block';btn.disabled=false;btn.innerHTML='<i class="fas fa-paper-plane"></i> إرسال الطلب'
}

async function handleContactSubmit(e){
e.preventDefault();
const btn=e.target.querySelector('button[type="submit"]');
const status=document.getElementById('contactStatus');
btn.disabled=true;btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> جاري الإرسال...';
status.className='form-status';status.style.display='none';
const data={
name:document.getElementById('cName').value.trim(),
email:document.getElementById('cEmail').value.trim(),
phone:document.getElementById('cPhone').value.trim(),
message:document.getElementById('cMessage').value.trim()
};
try{
const res=await fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
const result=await res.json();
if(res.ok){
status.className='form-status success';
status.textContent='✅ تم إرسال الرسالة! سنرد عليك قريباً.';
e.target.reset()
}else{throw new Error(result.error||'حدث خطأ')}
}catch(err){
status.className='form-status error';
status.textContent='❌ '+err.message
}status.style.display='block';btn.disabled=false;btn.innerHTML='<i class="fas fa-paper-plane"></i> إرسال الرسالة'
}

document.getElementById('quoteForm')?.addEventListener('submit',handleQuoteSubmit);
document.getElementById('contactForm')?.addEventListener('submit',handleContactSubmit);

document.querySelectorAll('a[href^="#"]').forEach(a=>{
a.addEventListener('click',e=>{
const id=a.getAttribute('href').slice(1);
if(id){const el=document.getElementById(id);if(el){e.preventDefault();el.scrollIntoView({behavior:'smooth',block:'start'})}}
})
});

const bgOrbs=document.querySelectorAll('.bg-orb');
const floatingShapes=document.querySelectorAll('.floating-shape');

const navbar=document.getElementById('navbar');
window.addEventListener('scroll',()=>{
const sY=window.scrollY;
navbar.classList.toggle('scrolled',sY>60);
bgOrbs.forEach((orb,i)=>{const speed=0.03*(i+1);orb.style.transform=`translateY(${sY*speed}px)`});
floatingShapes.forEach((shape,i)=>{const speed=0.02*(i+1);const dir=i%2===0?1:-1;shape.style.transform=`translate(${sY*speed*dir}px,${sY*speed*0.5}px)`});
if(sY<window.innerHeight)animateCounters()
});

const hamburger=document.getElementById('hamburger'),navLinks=document.getElementById('navLinks');
hamburger?.addEventListener('click',()=>{
hamburger.classList.toggle('active');navLinks.classList.toggle('open')
});
navLinks?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
hamburger?.classList.remove('active');navLinks?.classList.remove('open')
}));

let revealObserver;
function observeReveal(){
if(revealObserver)revealObserver.disconnect();
revealObserver=new IntersectionObserver((entries)=>{
entries.forEach(entry=>{
if(entry.isIntersecting){
entry.target.classList.add('visible');
const kids=entry.target.querySelectorAll('.reveal,.reveal-scale,.reveal-left,.reveal-right');
kids.forEach((k,j)=>{setTimeout(()=>k.classList.add('visible'),j*100)})
}
})
},{threshold:0.08});
document.querySelectorAll('.reveal,.reveal-scale,.reveal-left,.reveal-right').forEach(el=>revealObserver.observe(el))
}

function burstParticles(x,y,color='rgba(167,139,250'){
for(let i=0;i<12;i++){
const p={x:x,y:y,size:Math.random()*3+2,vx:(Math.random()-0.5)*6,vy:(Math.random()-0.5)*6,life:1};
const el=document.createElement('div');
el.style.cssText=`position:fixed;left:${x}px;top:${y}px;width:${p.size}px;height:${p.size}px;border-radius:50%;background:${color},0.8);pointer-events:none;z-index:9999;transition:all 0.6s cubic-bezier(0.25,0.46,0.45,0.94);opacity:1`;
document.body.appendChild(el);
requestAnimationFrame(()=>{el.style.transform=`translate(${p.vx*10}px,${p.vy*10}px) scale(0)`;el.style.opacity='0'});
setTimeout(()=>el.remove(),700)
}
}
document.addEventListener('click',e=>{
if(e.target.closest('.btn, .service-card, .portfolio-item, .giveaway-card, .hero-stat')){
burstParticles(e.clientX,e.clientY)
}
});

// ─── Back to Top ───
const backToTopBtn=document.createElement('button');
backToTopBtn.className='back-to-top';
backToTopBtn.innerHTML='<i class="fas fa-arrow-up"></i>';
backToTopBtn.setAttribute('aria-label','العودة للأعلى');
document.body.appendChild(backToTopBtn);

window.addEventListener('scroll',()=>{
backToTopBtn.classList.toggle('visible',window.scrollY>400)
});
backToTopBtn.addEventListener('click',()=>{
window.scrollTo({top:0,behavior:'smooth'})
});

// ─── Page Loader ───
const loader=document.querySelector('.page-loader');
if(loader){
window.addEventListener('load',()=>{
setTimeout(()=>loader.classList.add('hidden'),600)
});
// Fallback after 3s
setTimeout(()=>loader.classList.add('hidden'),3000)
}

// ─── Text Reveal ───
function initTextReveal(){
  document.querySelectorAll('.section-title').forEach(title=>{
    const fragments=[];
    Array.from(title.childNodes).forEach(node=>{
      if(node.nodeType===Node.TEXT_NODE){
        node.textContent.split(/(\s+)/).forEach(p=>fragments.push({text:p,type:'text'}))
      }else if(node.nodeType===Node.ELEMENT_NODE){
        fragments.push({text:node.outerHTML,type:'element'})
      }
    });
    let wordIdx=0;
    title.innerHTML=fragments.map(f=>{
      if(f.type==='element')return f.text;
      if(f.text.trim()==='')return f.text;
      return `<span class="text-reveal"><span class="text-reveal-inner text-reveal-delay-${wordIdx++%6}">${f.text}</span></span>`
    }).join('');
  });
  const textObserver=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.querySelectorAll('.text-reveal-inner').forEach((el,i)=>{
          setTimeout(()=>el.classList.add('visible'),i*60)
        });
        textObserver.unobserve(entry.target)
      }
    })
  },{threshold:0.1});
  document.querySelectorAll('.section-title').forEach(el=>textObserver.observe(el))
}

// ─── Testimonials ───
const testimonials=[
  {name:"أحمد الشريف",role:"صاحب شركة تكافل",text:"تعاملت مع زين ميديا في تصميم الهوية البصرية لشركتي. النتيجة كانت أفضل مما توقعت — احترافية، إبداع، ودقة في التنفيذ.",avatar:"أ"},
  {name:"نورة السعيد",role:"مديرة تسويق",text:"فريق محترف جداً. ساعدونا في إطلاق حملتنا الإعلانية وكان الأداء ممتاز. التفاعل زاد ٣٠٠٪!",avatar:"ن"},
  {name:"محمد الجابر",role:"صاحب مطعم مذاق",text:"تصاميمهم للمنيو والبروشورات كانت رائعة. خلّت المطعم يبان بشكل مختلف وجذاب. أنصح بالتعامل معهم.",avatar:"م"},
  {name:"سارة العمري",role:"مؤسسة متجر إلكتروني",text:"إدارة السوشيال ميديا عندهم شي خرافي. المتابعين زادوا والتفاعل صار أقوى. فريق متعاون ومبدع.",avatar:"س"},
  {name:"خالد الفوزان",role:"مدير شركة المنارة",text:"فيديو الافتتاح اللي سواه لنا كان تحفة. المونتاج والإخراج بشكل احترافي. سعر مقابل قيمة ممتاز.",avatar:"خ"},
  {name:"لمى بدر",role:"مصممة مستقلة",text:"طباعة الأوفسيت عندهم جودة عالية جداً. تعاملت معهم في طباعة كتيب فني والنتيجة كانت مبهرة.",avatar:"ل"},
  {name:"عبدالله القحطاني",role:"صاحب متجر مجوهرات",text:"حملة الدعاية والإعلان اللي عملوها لنا في رمضان كانت ناجحة جداً. المبيعات تضاعفت!",avatar:"ع"},
  {name:"هند المشاري",role:"مديرة مشاريع",text:"من أفضلال وكالات الإعلام اللي تعاملت معها. التزام بالمواعيد، إبداع في التصميم، وأسعار منافسة.",avatar:"ه"}
];
function renderTestimonials(){
  const section=document.createElement('section');section.id='testimonials';
  section.innerHTML=`
    <div class="container">
      <div class="section-label reveal">شهادات العملاء</div>
      <h2 class="section-title reveal">ماذا يقول <span class="highlight">عملاؤنا</span></h2>
      <p class="section-desc reveal">ثقة عملائنا هي رأس مالنا — شهادات من بعض من تعاملوا معنا</p>
      <div class="marquee-container">
        <div class="marquee-track">
          ${[...testimonials,...testimonials].map(t=>`
            <div class="testimonial-card">
              <i class="fas fa-quote-right quote-icon"></i>
              <p>${t.text}</p>
              <div class="testimonial-author">
                <div class="testimonial-avatar">${t.avatar}</div>
                <div><h4>${t.name}</h4><span>${t.role}</span></div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
  document.getElementById('giveaway').after(section);
  
}

// ─── Grid Background ───
function addGridBg(){
  const div=document.createElement('div');div.className='grid-bg';document.body.prepend(div)
}
addGridBg();

// ─── Section Dividers ───
function initSectionDividers(){
  document.querySelectorAll('section:not(:last-of-type)').forEach(sec=>{
    const divider=document.createElement('hr');divider.className='section-divider reveal';sec.after(divider)
  })
}

// ─── Glow Border on cards ───
function initGlowBorders(){
  document.querySelectorAll('.service-card,.giveaway-card').forEach(card=>card.classList.add('glow-border'))
}

renderServices();
renderMarketing();
renderFilters();
renderPortfolio('all');
renderGiveaway();
renderTestimonials();
observeReveal();
initTextReveal();
initSectionDividers();
initGlowBorders();
setTimeout(animateCounters,500);

document.querySelectorAll('.filter-btn').forEach(btn=>{
const match=btn.getAttribute('onclick')?.match(/filterPortfolio\('(\w+)'\)/);
if(match)btn.dataset.cat=match[1]
});

(function(){
const data={browser:'',browser_version:'',os:'',device:'',screen_size:screen.width+'x'+screen.height,language:navigator.language||'',referrer:document.referrer||'',page_visited:window.location.href};
const ua=navigator.userAgent;
data.user_agent=ua;
if(ua.includes('Chrome')&&!ua.includes('Edg')){data.browser='Chrome';const m=ua.match(/Chrome\/([\d.]+)/);if(m)data.browser_version=m[1]}
else if(ua.includes('Firefox')){data.browser='Firefox';const m=ua.match(/Firefox\/([\d.]+)/);if(m)data.browser_version=m[1]}
else if(ua.includes('Safari')&&!ua.includes('Chrome')){data.browser='Safari';const m=ua.match(/Version\/([\d.]+)/);if(m)data.browser_version=m[1]}
else if(ua.includes('Edg')){data.browser='Edge';const m=ua.match(/Edg\/([\d.]+)/);if(m)data.browser_version=m[1]}
else{data.browser='أخرى'}
if(ua.includes('Windows')){data.os='Windows'}
else if(ua.includes('Mac OS X')||ua.includes('macOS')){data.os='macOS'}
else if(ua.includes('Linux')&&!ua.includes('Android')){data.os='Linux'}
else if(ua.includes('Android')){data.os='Android';data.device='mobile'}
else if(ua.includes('iPhone')||ua.includes('iPad')){data.os='iOS';data.device='mobile'}
if(/Mobi|Android|iPhone|iPad|iPod/i.test(ua)){if(!data.device)data.device='mobile'}
if(/iPad|Tablet/i.test(ua)){data.device='tablet'}
if(!data.device)data.device='desktop';
fetch('/api/track',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).catch(()=>{});
if(navigator.geolocation){
navigator.geolocation.getCurrentPosition(pos=>{
fetch('/api/track',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lat:pos.coords.latitude,lng:pos.coords.longitude,country:'',city:''})}).catch(()=>{});
},()=>{}, {timeout:5000, enableHighAccuracy:false})
}
})();
