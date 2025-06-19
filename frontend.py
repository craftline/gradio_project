import gradio as gr
import requests

# Load custom theme
with open("theme.css", encoding="utf-8") as f:
    css = f.read()

# Load logo from base64 file
# with open("logo_base64.txt", "r", encoding="utf-8") as f:
#     logo_base64 = f.read().strip()

# Helper function to call backend
def process_backend(route, file_obj):
    if file_obj is None:
        return "لم يتم رفع أي ملف."
    try:
        with open(file_obj.name, "rb") as f:
            response = requests.post(
                url="http://localhost:8000/process",  # Change if hosted elsewhere
                files={"file": (file_obj.name, f, "application/pdf")},
                data={"route": route}
            )
        if response.status_code == 200:
            return response.text
        else:
            return f"خطأ: {response.json().get('error')}"
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بالخادم: {str(e)}"

# Page toggles
def show_home():
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

def show_app1():
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

def show_app2():
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

def show_app3():
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

def show_app4():
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

# Shared logo HTML with enhanced Arabic styling
logo_html = f"""
<div class="header">
  <div class="title">برامج الذكاء الاصطناعي لأعمال اللجان</div>
  <div class="logo">
    <img src="" alt="الشعار" />
  </div>
</div>
<hr class="separator" />
"""

# Custom CSS for better Arabic support
arabic_css = """
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');

.gradio-container {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Cairo', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

/* RTL support for all components */
.gradio-container * {
    direction: rtl !important;
    text-align: right !important;
}

/* Button styling for Arabic */
button {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
}

/* Textbox styling for Arabic */
textarea, input[type="text"] {
    font-family: 'Cairo', sans-serif !important;
    text-align: right !important;
    direction: rtl !important;
}

/* Label styling for Arabic */
label {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    text-align: right !important;
}

/* Markdown styling for Arabic */
.markdown-text {
    font-family: 'Cairo', sans-serif !important;
    text-align: right !important;
    direction: rtl !important;
}

/* File upload styling */
.file-upload {
    direction: rtl !important;
    text-align: right !important;
}

/* Navigation buttons */
.nav-button {
    background-color: #143B9A !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.nav-button:hover {
    background-color: #0d2b6b !important;
    transform: translateY(-2px) !important;
}

/* Process button styling */
.process-button {
    background-color: #28a745 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin-top: 10px !important;
}

.process-button:hover {
    background-color: #218838 !important;
    transform: translateY(-2px) !important;
}

/* Back button styling */
.back-button {
    background-color: #6c757d !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin-top: 20px !important;
}

.back-button:hover {
    background-color: #545b62 !important;
    transform: translateY(-2px) !important;
}

/* Loading animation for Arabic */
.loading {
    text-align: center !important;
    direction: rtl !important;
    font-family: 'Cairo', sans-serif !important;
}

/* Error messages in Arabic */
.error-message {
    color: #dc3545 !important;
    font-family: 'Cairo', sans-serif !important;
    text-align: right !important;
    direction: rtl !important;
}

/* Success messages in Arabic */
.success-message {
    color: #28a745 !important;
    font-family: 'Cairo', sans-serif !important;
    text-align: right !important;
    direction: rtl !important;
}
"""

with gr.Blocks(css=css + arabic_css, title="برامج الذكاء الاصطناعي لأعمال اللجان") as demo:
    app1 = gr.Column(visible=False)
    app2 = gr.Column(visible=False)
    app3 = gr.Column(visible=False)
    app4 = gr.Column(visible=False)
    home = gr.Column(visible=True)

    # HOME PAGE
    with home:
        gr.HTML(logo_html)

        with gr.Row(elem_classes="row"):
            btn1 = gr.Button("📄 تلخيص الملفات العربية", elem_classes="box")
            btn2 = gr.Button("📄 تلخيص الملفات الإنجليزية", elem_classes="box")

        with gr.Row(elem_classes="row"):
            btn3 = gr.Button("🌐 الترجمة إلى اللغة العربية", elem_classes="box")
            btn4 = gr.Button("🌐 الترجمة إلى اللغة الإنجليزية", elem_classes="box")

    # APP 1 - Arabic Summarization
    with app1:
        gr.HTML(logo_html)
        gr.Markdown("### 📄 تلخيص الملفات العربية", elem_classes="markdown-text")
        gr.Markdown("قم برفع ملف PDF أو Word للحصول على ملخص باللغة العربية", elem_classes="markdown-text")
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input1 = gr.File(
                    label="📁 ارفع ملفك هنا",
                    file_types=[".pdf", ".docx", ".doc"],
                    elem_classes="file-upload"
                )
            with gr.Column(scale=1):
                gr.Markdown("""
                **الملفات المدعومة:**
                - ملفات PDF
                - ملفات Word (.docx, .doc)
                
                **الحد الأقصى:** 10 ميجابايت
                """, elem_classes="markdown-text")
        
        output_box1 = gr.Textbox(
            label="📋 النتيجة",
            lines=15,
            placeholder="ستظهر النتيجة هنا بعد المعالجة..."
        )
        
        with gr.Row():
            gr.Button("🚀 تشغيل النموذج", elem_classes="process-button").click(
                fn=lambda f: process_backend("A", f), 
                inputs=[file_input1], 
                outputs=[output_box1]
            )
            gr.Button("⬅ العودة للصفحة الرئيسية", elem_classes="back-button").click(
                fn=show_home, 
                outputs=[home, app1, app2, app3, app4]
            )

    # APP 2 - English Summarization
    with app2:
        gr.HTML(logo_html)
        gr.Markdown("### 📄 تلخيص الملفات الإنجليزية", elem_classes="markdown-text")
        gr.Markdown("قم برفع ملف PDF أو Word للحصول على ملخص باللغة الإنجليزية", elem_classes="markdown-text")
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input2 = gr.File(
                    label="📁 ارفع ملفك هنا",
                    file_types=[".pdf", ".docx", ".doc"],
                    elem_classes="file-upload"
                )
            with gr.Column(scale=1):
                gr.Markdown("""
                **الملفات المدعومة:**
                - ملفات PDF
                - ملفات Word (.docx, .doc)
                
                **الحد الأقصى:** 10 ميجابايت
                """, elem_classes="markdown-text")
        
        output_box2 = gr.Textbox(
            label="📋 النتيجة",
            lines=15,
            placeholder="ستظهر النتيجة هنا بعد المعالجة..."
        )
        
        with gr.Row():
            gr.Button("🚀 تشغيل النموذج", elem_classes="process-button").click(
                fn=lambda f: process_backend("B", f), 
                inputs=[file_input2], 
                outputs=[output_box2]
            )
            gr.Button("⬅ العودة للصفحة الرئيسية", elem_classes="back-button").click(
                fn=show_home, 
                outputs=[home, app1, app2, app3, app4]
            )

    # APP 3 - English to Arabic Translation
    with app3:
        gr.HTML(logo_html)
        gr.Markdown("### 🌐 ترجمة الملفات الإنجليزية إلى العربية", elem_classes="markdown-text")
        gr.Markdown("قم برفع ملف باللغة الإنجليزية للحصول على ترجمة باللغة العربية", elem_classes="markdown-text")
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input3 = gr.File(
                    label="📁 ارفع ملفك هنا",
                    file_types=[".pdf", ".docx", ".doc", ".txt"],
                    elem_classes="file-upload"
                )
            with gr.Column(scale=1):
                gr.Markdown("""
                **الملفات المدعومة:**
                - ملفات PDF
                - ملفات Word (.docx, .doc)
                - ملفات نصية (.txt)
                
                **الحد الأقصى:** 10 ميجابايت
                """, elem_classes="markdown-text")
        
        output_box3 = gr.Textbox(
            label="📋 الترجمة",
            lines=15,
            placeholder="ستظهر الترجمة هنا بعد المعالجة..."
        )
        
        with gr.Row():
            gr.Button("🚀 تشغيل النموذج", elem_classes="process-button").click(
                fn=lambda f: process_backend("C", f), 
                inputs=[file_input3], 
                outputs=[output_box3]
            )
            gr.Button("⬅ العودة للصفحة الرئيسية", elem_classes="back-button").click(
                fn=show_home, 
                outputs=[home, app1, app2, app3, app4]
            )

    # APP 4 - Arabic to English Translation
    with app4:
        gr.HTML(logo_html)
        gr.Markdown("### 🌐 ترجمة الملفات العربية إلى الإنجليزية", elem_classes="markdown-text")
        gr.Markdown("قم برفع ملف باللغة العربية للحصول على ترجمة باللغة الإنجليزية", elem_classes="markdown-text")
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input4 = gr.File(
                    label="📁 ارفع ملفك هنا",
                    file_types=[".pdf", ".docx", ".doc", ".txt"],
                    elem_classes="file-upload"
                )
            with gr.Column(scale=1):
                gr.Markdown("""
                **الملفات المدعومة:**
                - ملفات PDF
                - ملفات Word (.docx, .doc)
                - ملفات نصية (.txt)
                
                **الحد الأقصى:** 10 ميجابايت
                """, elem_classes="markdown-text")
        
        output_box4 = gr.Textbox(
            label="📋 الترجمة",
            lines=15,
            placeholder="ستظهر الترجمة هنا بعد المعالجة..."
        )
        
        with gr.Row():
            gr.Button("🚀 تشغيل النموذج", elem_classes="process-button").click(
                fn=lambda f: process_backend("D", f), 
                inputs=[file_input4], 
                outputs=[output_box4]
            )
            gr.Button("⬅ العودة للصفحة الرئيسية", elem_classes="back-button").click(
                fn=show_home, 
                outputs=[home, app1, app2, app3, app4]
            )

    # Navigation
    btn1.click(fn=show_app1, outputs=[home, app1, app2, app3, app4])
    btn2.click(fn=show_app2, outputs=[home, app1, app2, app3, app4])
    btn3.click(fn=show_app3, outputs=[home, app1, app2, app3, app4])
    btn4.click(fn=show_app4, outputs=[home, app1, app2, app3, app4])

# Launch with Arabic-friendly settings
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    show_error=True,
    quiet=False
)
