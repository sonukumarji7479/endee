import os
import re

chat_path = r"c:\Users\sonuk\Desktop\ai boot\frontend\pages\chat.js"
dash_path = r"c:\Users\sonuk\Desktop\ai boot\frontend\pages\dashboard.js"

# 1. FIX chat.js
if os.path.exists(chat_path):
    with open(chat_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace let answer = data.answer; with let answer = data.data;
    content = content.replace("let answer = data.answer;", "let answer = data.data;")
    
    # Replacement for appendMessage body
    append_msg_code = """    function appendMessage(sender, text) {
         const div = document.createElement('div');
         div.className = `message ${sender}`;
         div.style.cssText = `
             padding: 12px 16px; border-radius: 12px; max-width: 85%; font-size: 0.9rem; line-height: 1.4;
             ${sender==='assistant' ? 'background:rgba(255,255,255,0.03); align-self:flex-start;' : 'background:#58a6ff; color:#0d1117; align-self:flex-end;'}
         `;
         
         let htmlContent = text;
         let speakText = text;

         if (typeof text === 'object' && text.sections) {
              // Structured response rendering
              let html = `<h4 style="color:var(--accent-color); margin-bottom:12px; font-size:1.1rem;">${text.title || 'Summary'}</h4>`;
              html += `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; margin-top: 10px;">`;
              
              text.sections.forEach(sec => {
                  html += `
                      <div class="glass-panel" style="padding: 16px; border-radius: 12px; background: rgba(255,255,255,0.01); border: 1px solid var(--border-color); display:flex; flex-direction:column; gap:8px;">
                          <div style="font-weight: 600; font-size: 0.85rem; color: #58a6ff; text-transform: uppercase; letter-spacing: 0.5px;">${sec.heading}</div>
                          <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5; flex:1;">${sec.content}</div>
                      </div>
                  `;
              });
              html += `</div>`;
              htmlContent = html;
              speakText = `Responding regarding ${text.title || 'topic'}. Sections include ${text.sections.map(s => s.heading).join(', ')}`;
         }

         if (sender === 'assistant') {
              div.innerHTML = `
                  <div class="message-text">${typeof htmlContent === 'string' ? htmlContent : JSON.stringify(htmlContent)}</div>
                  <button class="speak-btn" style="background:transparent; border:none; color:var(--text-secondary); cursor:pointer; font-size:0.75rem; margin-top:8px; display:flex; align-items:center; gap:4px;"><i class="fa-solid fa-volume-high"></i> Listen</button>
              `;
              div.querySelector('.speak-btn').addEventListener('click', () => {
                   const utt = new SpeechSynthesisUtterance(speakText);
                   const langSelect = document.getElementById('app-language');
                   if (langSelect) utt.lang = langSelect.value;
                   window.speechSynthesis.speak(utt);
              });
         } else {
              div.innerText = text;
         }

         const chatMessages = document.getElementById('chat-messages');
         if (chatMessages) {
              chatMessages.appendChild(div);
              chatMessages.scrollTop = chatMessages.scrollHeight;
         }
    }"""
    
    # Use re to replace appendMessage Wholesale
    # Match from "function appendMessage" up to "chatMessages.scrollTop = ... }"
    content = re.sub(
        r"function appendMessage\(sender, text\)\s*\{[\s\S]*?chatMessages\.scrollTop = chatMessages\.scrollHeight;\s*\}",
        append_msg_code,
        content
    )
    
    with open(chat_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("chat.js updated")

# 2. FIX dashboard.js
if os.path.exists(dash_path):
    with open(dash_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace data.answer to data.data
    content = content.replace("appendQuickMsg('assistant', data.answer || \"No response.\");", "appendQuickMsg('assistant', data.data || \"No response.\");")
    
    # Replacement for appendQuickMsg
    append_quick_code = """    function appendQuickMsg(sender, text) {
        const div = document.createElement('div');
        div.style.cssText = `background: ${sender==='assistant' ? 'rgba(255,255,255,0.03)' : '#58a6ff'}; color: ${sender==='assistant' ? 'white' : '#0d1117'}; padding: 12px; border-radius: 12px; align-self: ${sender==='assistant' ? 'flex-start' : 'flex-end'}; max-width: ${sender==='assistant' ? '90%' : '80%'};`;
        
        if (typeof text === 'object' && text.sections) {
             let html = `<div style="font-weight:600; color:var(--accent-color); margin-bottom:8px; font-size:1rem;">${text.title || 'Summary'}</div>`;
             html += `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">`;
             text.sections.forEach(sec => {
                 html += `
                     <div style="background: rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 12px;">
                         <div style="font-size: 0.75rem; color: #58a6ff; font-weight:600; margin-bottom:4px;">${sec.heading}</div>
                         <div style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4;">${sec.content}</div>
                     </div>
                 `;
             });
             html += `</div>`;
             div.innerHTML = html;
        } else {
             div.innerText = typeof text === 'string' ? text : JSON.stringify(text);
        }

        const quickMessages = document.getElementById('quick-chat-messages');
        if (quickMessages) {
             quickMessages.appendChild(div);
             quickMessages.scrollTop = quickMessages.scrollHeight;
        }
    }"""
    
    # Replace appendQuickMsg
    content = re.sub(
        r"function appendQuickMsg\(sender, text\)\s*\{[\s\S]*?quickMessages\.scrollTop = quickMessages\.scrollHeight;\s*\}",
        append_quick_code,
        content
    )
    
    with open(dash_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("dashboard.js updated")
