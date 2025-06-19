import gradio as gr
import requests

# Load custom theme
with open("theme.css", encoding="utf-8") as f:
    css = f.read()

# Load logo from base64 file
with open("logo_base64.txt", "r", encoding="utf-8") as f:
    logo_base64 = f.read().strip()

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

# Shared logo HTML
logo_html = f"""
<div class="header">
  <div class="title">برامج الذكاء الاصطناعي لأعمال اللجان</div>
  <div class="logo">
    <img src="{logo_base64}" alt="Logo" />
  </div>
</div>
<hr class="separator" />
"""

with gr.Blocks(css=css) as demo:
    app1 = gr.Column(visible=False)
    app2 = gr.Column(visible=False)
    app3 = gr.Column(visible=False)
    app4 = gr.Column(visible=False)
    home = gr.Column(visible=True)

    # HOME PAGE
    with home:
        gr.HTML(logo_html)

        with gr.Row(elem_classes="row"):
            btn1 = gr.Button("تلخيص الملفات العربية", elem_classes="box")
            btn2 = gr.Button("تلخيص الملفات الانجليزية", elem_classes="box")

        with gr.Row(elem_classes="row"):
            btn3 = gr.Button("الترجمة إلى اللغة العربية", elem_classes="box")
            btn4 = gr.Button("الترجمة إلى اللغة الإنجليزية", elem_classes="box")

    # APP 1
    with app1:
        gr.HTML(logo_html)
        gr.Markdown("### تلخيص الملفات العربية")
        gr.Markdown("تلخيص الملفات باللغة العربية")
        file_input1 = gr.File(label="ارفع ملفك هنا")
        output_box1 = gr.Textbox(label="المخرجات", lines=10)
        gr.Button("تشغيل النموذج").click(fn=lambda f: process_backend("A", f), inputs=[file_input1], outputs=[output_box1])
        gr.Button("⬅ العودة").click(fn=show_home, outputs=[home, app1, app2, app3, app4])

    # APP 2
    with app2:
        gr.HTML(logo_html)
        gr.Markdown("### تخليص الملفات الانجليزية")
        gr.Markdown("تلخيص الملفات الانجليزية")
        file_input2 = gr.File(label="ارفع ملفك هنا")
        output_box2 = gr.Textbox(label="المخرجات", lines=10)
        gr.Button("تشغيل النموذج").click(fn=lambda f: process_backend("B", f), inputs=[file_input2], outputs=[output_box2])
        gr.Button("⬅ العودة").click(fn=show_home, outputs=[home, app1, app2, app3, app4])

    # APP 3
    with app3:
        gr.HTML(logo_html)
        gr.Markdown("### ترجمة الملفات الإنجليزية إلى العربية")
        gr.Markdown("ترجمة الملفات الإنجليزية إلى العربية")
        file_input3 = gr.File(label="ارفع ملفك هنا")
        output_box3 = gr.Textbox(label="المخرجات", lines=10)
        gr.Button("تشغيل النموذج").click(fn=lambda f: process_backend("C", f), inputs=[file_input3], outputs=[output_box3])
        gr.Button("⬅ العودة").click(fn=show_home, outputs=[home, app1, app2, app3, app4])

    # APP 4
    with app4:
        gr.HTML(logo_html)
        gr.Markdown("### ترجمة الملفات العربية إلى الإنجليزية")
        gr.Markdown("ترجمة الملفات الإنجليزية إلى العربية")
        file_input4 = gr.File(label="ارفع ملفك هنا")
        output_box4 = gr.Textbox(label="المخرجات", lines=10)
        gr.Button("تشغيل النموذج").click(fn=lambda f: process_backend("D", f), inputs=[file_input4], outputs=[output_box4])
        gr.Button("⬅ العودة").click(fn=show_home, outputs=[home, app1, app2, app3, app4])

    # Navigation
    btn1.click(fn=show_app1, outputs=[home, app1, app2, app3, app4])
    btn2.click(fn=show_app2, outputs=[home, app1, app2, app3, app4])
    btn3.click(fn=show_app3, outputs=[home, app1, app2, app3, app4])
    btn4.click(fn=show_app4, outputs=[home, app1, app2, app3, app4])

demo.launch()
