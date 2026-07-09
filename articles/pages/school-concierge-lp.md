---
title: 【無料60秒診断】あなたに合うスクールをコンシェルジュがご提案
slug: school-concierge-lp
type: page
body_class: lp-page
excerpt: 4つの質問に答えるだけで、あなたに合うAIスクール・プログラミングスクールをコンシェルジュが無料診断。補助金で最大80%OFFになるかもその場でわかります。
---

<div class="cx-app">
<div class="cx-header">
<p class="cx-badge">無料・約60秒で完了</p>
<p class="cx-title">あなたにぴったりのスクール、<br>コンシェルジュが診断します</p>
<div class="cx-progress"><div class="cx-progress-bar" id="cxBar"></div></div>
<p class="cx-progress-label" id="cxStep">質問 1 / 4</p>
</div>
<div class="cx-stage">
<div class="cx-left">
<div class="cx-qpanel" id="cxPanel">
<p class="cx-question" id="cxQ"></p>
<div class="cx-choices" id="cxChoices"></div>
</div>
<div class="cx-loading" id="cxLoading" style="display:none;">
<div class="cx-loading-dots"><span></span><span></span><span></span></div>
<p class="cx-loading-text">あなたに合うスクールを選定しています…</p>
</div>
<div id="cxResult" style="display:none;">
<p class="cx-result-title">診断結果：あなたにおすすめの2校</p>
<div id="cxCards"></div>
<button type="button" class="cx-restart" id="cxRestart">もう一度診断する</button>
</div>
</div>
<div class="cx-right">
<div class="cx-bubble" id="cxBubble"><p id="cxBubbleText">こんにちは！担当コンシェルジュです。4つの質問に答えるだけで、あなたに合うスクールを2校ご提案します。まずは最初の質問からどうぞ。</p></div>
<div class="cx-char" id="cxChar">
<svg viewBox="0 0 200 225" aria-hidden="true" focusable="false">
<path d="M42 225 C42 176 70 152 100 152 C130 152 158 176 158 225 Z" fill="#0f2c4d"/>
<path d="M86 156 L100 178 L114 156 L100 166 Z" fill="#ffffff"/>
<rect x="96" y="176" width="8" height="14" rx="3" fill="#ff5b39"/>
<circle cx="100" cy="96" r="47" fill="#f8d8c2"/>
<path d="M53 92 C53 58 76 40 100 40 C124 40 147 58 147 92 C138 64 121 55 100 55 C79 55 62 64 53 92 Z" fill="#333a45"/>
<ellipse class="cx-eye" cx="83" cy="97" rx="4.5" ry="5.5" fill="#2b2f36"/>
<ellipse class="cx-eye" cx="117" cy="97" rx="4.5" ry="5.5" fill="#2b2f36"/>
<circle cx="72" cy="111" r="6" fill="#f3b39a" opacity="0.55"/>
<circle cx="128" cy="111" r="6" fill="#f3b39a" opacity="0.55"/>
<path d="M89 116 Q100 127 111 116" stroke="#c96f4a" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>
</div>
<p class="cx-char-name">スクール診断コンシェルジュ</p>
</div>
</div>
<p class="cx-note">本診断は当サイト編集部の基準に基づくもので、特定スクールの受講を保証・強制するものではありません。本ページはプロモーション（広告）を含みます。補助金・給付金の受給可否は各制度の要件およびハローワーク等の審査により決まります。</p>
</div>

<script>(function(){ var $=function(id){return document.getElementById(id);}; var AFF={ kikagaku:"", shiftai:"", dmmai:"", webcamp:"", techcamp:"", samurai:"", daytra:"" }; var FALLBACK={ kikagaku:"/ai-reskilling-subsidy/", shiftai:"/shift-ai-review/" }; var SCHOOLS={ kikagaku:{name:"キカガク 長期コース",tag:"AI・データサイエンス／6ヶ月",subsidy:true,reason:"転職支援つきでAI・データサイエンスを体系的に学べます。専門実践教育訓練給付金の対象講座のため、条件を満たせば受講料の最大80%が支給される可能性があります。"}, shiftai:{name:"SHIFT AI",tag:"生成AI活用／月額制",subsidy:false,reason:"月額制で初期投資を抑えて始められる生成AI特化スクール。ChatGPTから画像・動画生成まで動画1,000本以上が学び放題で、副業・業務効率化との相性が抜群です。"}, dmmai:{name:"DMM 生成AI CAMP",tag:"生成AI活用／短期集中",subsidy:true,reason:"生成AIをビジネス実務に落とし込む短期集中型。プロンプト設計から業務活用まで実践重視で、リスキリング補助金の対象コースが用意されています。"}, webcamp:{name:"DMM WEBCAMP",tag:"プログラミング／転職特化",subsidy:true,reason:"転職成功実績が豊富な転職特化型スクール。専属キャリアアドバイザーの支援と教育訓練給付金対象コースで、未経験からのエンジニア転職を現実にします。"}, techcamp:{name:"テックキャンプ",tag:"プログラミング／短期集中",subsidy:true,reason:"未経験からの短期集中学習に定評のある大手スクール。教育訓練給付金の対象で、キャリア面談から転職まで一気通貫のサポートが受けられます。"}, samurai:{name:"侍エンジニア",tag:"マンツーマン／オーダーメイド",subsidy:true,reason:"現役エンジニアのマンツーマン指導で、目的に合わせたオーダーメイドカリキュラムを組めるのが最大の強み。挫折率の低さに定評があります。"}, daytra:{name:"デイトラ",tag:"買い切り／低価格",subsidy:false,reason:"10万円前後の買い切り型で、副業向けスキルをコスパ良く学べる人気スクール。教材は買い切り後もアップデートされ、自分のペースで進められます。"} }; var QUESTIONS=[ {key:"subsidy",q:"国の補助金で受講料が最大80%戻る制度、もし使えるなら使いたいですか？",choices:[ {v:"yes",label:"ぜひ使いたい",react:"賢明です！実はこの制度、知らずに全額自己負担で申し込む方がとても多いんです。あなたが対象になるか、次の質問で確認しますね。"}, {v:"learn",label:"制度をよく知らなかった",react:"お伝えできてよかったです。79万円の講座が実質15.8万円になるケースもある制度なんです。対象かどうか、一緒に確認しましょう。"}, {v:"no",label:"使えなくてもいい（早く始めたい）",react:"承知しました。スピード感を大事に、面倒な手続きなしですぐ始められるスクールを中心にご提案しますね。"} ]}, {key:"work",q:"現在のお仕事の状況を教えてください。",choices:[ {v:"emp1y",label:"会社員・公務員（勤続1年以上）",react:"ありがとうございます。補助金の対象になる可能性が高い状況です。これは大きなアドバンテージですよ。"}, {v:"empShort",label:"会社員（1年未満）・パート",react:"ありがとうございます。雇用保険の加入期間によっては対象になる場合があります。対象外でも低コストで始められる選択肢をご用意しますね。"}, {v:"free",label:"フリーランス・自営業",react:"ありがとうございます。給付金の対象からは外れますが、その分、月額制などの身軽な選択肢がフィットしやすいですよ。"}, {v:"leaving",label:"離職中・転職活動中",react:"ありがとうございます。実は離職中の方が使える支援制度もあるんです。学び直しには良いタイミングかもしれません。"} ]}, {key:"field",q:"どちらの分野に、より興味がありますか？",choices:[ {v:"ai",label:"AI活用（ChatGPT・画像生成など）",react:"いい選択です。AI活用スキルは2026年、職種を問わず最も需要が伸びている分野です。"}, {v:"prog",label:"プログラミング・システム開発",react:"王道ですね。開発スキルは求人数が多く、キャリアの選択肢が一気に広がります。"}, {v:"unsure",label:"迷っている・どちらも気になる",react:"正直で素晴らしいです。実は目的から逆算すると自然に決まるんです。次の質問で絞り込みますね。"} ]}, {key:"goal",q:"スキルを身につけて、実現したいことは？",choices:[ {v:"career",label:"転職・キャリアチェンジ",react:"本気の一歩ですね。転職支援の実績があるスクールをご提案します。"}, {v:"side",label:"副業で収入を増やしたい",react:"堅実です。低リスクで始めて、実践で稼ぎながら学べる形が合いそうです。"}, {v:"current",label:"今の仕事で評価を上げたい",react:"素晴らしい。現職×新スキルは、最も再現性の高いキャリア戦略です。"}, {v:"vague",label:"まだ漠然と・将来への備え",react:"その感覚、大事です。まず小さく始めて手応えを掴める形をご提案しますね。"} ]} ]; function recommend(a){ if(a.field==="ai"){return a.goal==="career"?["kikagaku","samurai"]:["shiftai","dmmai"];} if(a.field==="prog"){return a.goal==="career"?["webcamp","techcamp"]:["samurai","daytra"];} if(a.goal==="career"){return ["kikagaku","webcamp"];} if(a.goal==="current"){return ["shiftai","samurai"];} return ["shiftai","daytra"]; } var state={step:0,ans:{}}; var busy=false; function renderQ(){ var qd=QUESTIONS[state.step]; $("cxQ").textContent=qd.q; var wrap=$("cxChoices"); wrap.innerHTML=""; qd.choices.forEach(function(c){ var b=document.createElement("button"); b.type="button"; b.className="cx-choice"; b.innerHTML="<span>"+c.label+"</span><span class=\"cx-check\"><svg viewBox=\"0 0 16 16\" fill=\"none\"><path d=\"M3 8.5L6.5 12L13 4.5\" stroke=\"currentColor\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg></span>"; b.addEventListener("click",function(){pick(b,qd,c);}); wrap.appendChild(b); }); var p=$("cxPanel"); p.classList.remove("cx-qpanel"); void p.offsetWidth; p.classList.add("cx-qpanel"); $("cxStep").textContent="質問 "+(state.step+1)+" / 4"; } function speak(text){ var bub=$("cxBubble"); bub.classList.add("is-swap"); setTimeout(function(){ $("cxBubbleText").textContent=text; bub.classList.remove("is-swap"); },220); } function nod(){ var ch=$("cxChar"); ch.classList.remove("is-nod"); void ch.offsetWidth; ch.classList.add("is-nod"); } function pick(btn,qd,c){ if(busy){return;} busy=true; state.ans[qd.key]=c.v; var siblings=$("cxChoices").children; for(var i=0;i<siblings.length;i++){ if(siblings[i]!==btn){siblings[i].classList.add("is-faded");} } btn.classList.add("is-picked"); nod(); setTimeout(function(){speak(c.react);},300); $("cxBar").style.width=(((state.step+1)/4)*100)+"%"; setTimeout(function(){ busy=false; if(state.step<QUESTIONS.length-1){ state.step++; renderQ(); }else{ diagnose(); } },1100); } function schoolUrl(id){ if(AFF[id]){return AFF[id];} if(FALLBACK[id]){return FALLBACK[id];} return ""; } function eligible(){ return state.ans.work==="emp1y"||state.ans.work==="leaving"; } function diagnose(){ $("cxPanel").style.display="none"; $("cxLoading").style.display="flex"; $("cxStep").textContent="診断中…"; speak("回答ありがとうございました。あなたの状況に合わせて、最適な2校を選定しています…"); setTimeout(function(){ $("cxLoading").style.display="none"; showResult(); },1400); } function showResult(){ var ids=recommend(state.ans); var wrap=$("cxCards"); wrap.innerHTML=""; ids.forEach(function(id,idx){ var s=SCHOOLS[id]; var card=document.createElement("div"); card.className="cx-card"; var badge=(eligible()&&s.subsidy)?"<span class=\"cx-card-badge\">補助金対象の可能性あり（最大80%支給）</span>":""; var extra=(eligible()&&s.subsidy)?"あなたの回答から、給付金の対象になる可能性が高い状況です。無料カウンセリングで受給条件を必ず確認してください。":""; var url=schoolUrl(id); var cta=url?("<a class=\"cx-card-cta\" href=\""+url+"\" rel=\"nofollow sponsored\">詳しく見る（無料）</a>"):("<span class=\"cx-card-cta is-pending\">近日リンク公開</span>"); card.innerHTML="<span class=\"cx-card-rank\">おすすめ "+(idx+1)+"</span><p class=\"cx-card-name\">"+s.name+"</p><p class=\"cx-card-tag\">"+s.tag+"</p>"+badge+"<p class=\"cx-card-reason\">"+s.reason+(extra?" "+extra:"")+"</p>"+cta; wrap.appendChild(card); setTimeout(function(){card.classList.add("is-in");},150+idx*220); }); $("cxResult").style.display="block"; $("cxStep").textContent="診断完了"; speak("お待たせしました。あなたの回答から、この2校が最有力です。どちらも無料で詳細を確認できるので、まずは比べてみてください。"); } $("cxRestart").addEventListener("click",function(){location.reload();}); renderQ(); })();</script>
