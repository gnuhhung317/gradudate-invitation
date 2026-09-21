import os
import time
from playwright.sync_api import sync_playwright

def run():
    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    html_path = f"file:///{os.path.abspath('index.html').replace('\\', '/')}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 375, "height": 812})
        page.goto(html_path)
        page.wait_for_load_state("networkidle")
        time.sleep(1)

        # 1. Test Default Export
        with page.expect_download() as download_info:
            page.click("#download-btn")
        download = download_info.value
        export_path_default = os.path.join(screenshots_dir, "exported_default.png")
        download.save_as(export_path_default)
        print(f"Default Export saved: {export_path_default}")

        # 2. Test Custom Name Export
        page.fill("#name-input", "Anh Nguyễn Văn Hoàng Nam")
        time.sleep(0.5)
        with page.expect_download() as download_info:
            page.click("#download-btn")
        download_custom = download_info.value
        export_path_custom = os.path.join(screenshots_dir, "exported_custom_name.png")
        download_custom.save_as(export_path_custom)
        print(f"Custom Name Export saved: {export_path_custom}")

        browser.close()

if __name__ == "__main__":
    run()
