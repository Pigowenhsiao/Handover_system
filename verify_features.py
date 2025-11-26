"""
電子交接系統功能實現檢查
確認電子交接系統的核心功能已實現
"""
import os
import sys
from pathlib import Path


def check_backend_core_components():
    """檢查後端核心組件"""
    print("檢查後端核心組件...")
    
    # 檢查配置文件
    config_path = "backend/core/config.py"
    if os.path.exists(config_path):
        print("✓ 後端配置文件存在")
    else:
        print("✗ 後端配置文件不存在")
    
    # 檢查安全模塊
    security_path = "backend/core/security.py"
    if os.path.exists(security_path):
        print("✓ 後端安全模塊存在")
    else:
        print("✗ 後端安全模塊不存在")
    
    # 檢查數據庫相關文件
    db_files = [
        "backend/database/base.py",
        "backend/database/session.py",
        "backend/database/init_db.py"
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"✓ {db_file} 存在")
        else:
            print(f"✗ {db_file} 不存在")


def check_frontend_components():
    """檢查前端組件"""
    print("\n檢查前端組件...")
    
    # 檢查前端語言管理器
    frontend_lang_path = "frontend/i18n/language_manager.py"
    if os.path.exists(frontend_lang_path):
        print("✓ 前端語言管理器存在")
    else:
        print("✗ 前端語言管理器不存在")
    
    # 檢查前端語言選擇器
    lang_selector_path = "frontend/src/components/language_selector.py"
    if os.path.exists(lang_selector_path):
        print("✓ 語言選擇器組件存在")
    else:
        print("✗ 語言選擇器組件不存在")
    
    # 檢查前端出勤記錄組件
    attendance_path = "frontend/src/components/attendance_section.py"
    if os.path.exists(attendance_path):
        print("✓ 出勤記錄組件存在")
    else:
        print("✗ 出勤記錄組件不存在")
    
    # 檢查前端主應用程式
    main_path = "frontend/main.py"
    if os.path.exists(main_path):
        print("✓ 前端主應用程式存在")
    else:
        print("✗ 前端主應用程式不存在")


def check_models_and_schemas():
    """檢查數據模型和架構"""
    print("\n檢查數據模型和架構...")

    # 檢查後端模型
    model_paths = [
        "backend/models/all_models.py"
    ]

    for model_path in model_paths:
        if os.path.exists(model_path):
            print(f"✓ {model_path} 存在")
        else:
            print(f"✗ {model_path} 不存在")

    # 檢查後端架構
    schema_paths = [
        "backend/schemas/user.py",
        "backend/schemas/report.py",
        "backend/schemas/attendance.py",
        "backend/schemas/equipment.py",
        "backend/schemas/lot.py",
        "backend/schemas/language.py"
    ]

    for schema_path in schema_paths:
        if os.path.exists(schema_path):
            print(f"✓ {schema_path} 存在")
        else:
            print(f"✗ {schema_path} 不存在")


def check_api_endpoints():
    """檢查 API 端點"""
    print("\n檢查 API 端點...")
    
    endpoint_paths = [
        "backend/api/v1/endpoints/auth.py",
        "backend/api/v1/endpoints/users.py",
        "backend/api/v1/endpoints/reports.py",
        "backend/api/v1/endpoints/attendance.py",
        "backend/api/v1/endpoints/equipment.py",
        "backend/api/v1/endpoints/lots.py",
        "backend/api/v1/endpoints/languages.py"
    ]
    
    for endpoint_path in endpoint_paths:
        if os.path.exists(endpoint_path):
            print(f"✓ {endpoint_path} 存在")
        else:
            print(f"✗ {endpoint_path} 不存在")


def check_spec_documents():
    """檢查規格文件"""
    print("\n檢查規格文件...")
    
    spec_paths = [
        "specs/01_multi-language-support/spec.md",
        "specs/02_multilang-labels/spec.md",
        "specs/03_attendance-enhancement/spec.md"
    ]
    
    for spec_path in spec_paths:
        if os.path.exists(spec_path):
            print(f"✓ {spec_path} 存在")
        else:
            print(f"✗ {spec_path} 不存在")


def check_language_resources():
    """檢查語言資源文件"""
    print("\n檢查語言資源文件...")
    
    locales_dir = "frontend/public/locales"
    if os.path.exists(locales_dir):
        print("✓ 語言資源目錄存在")
        
        lang_files = ["ja.json", "zh.json", "en.json"]
        for lang_file in lang_files:
            file_path = os.path.join(locales_dir, lang_file)
            if os.path.exists(file_path):
                print(f"✓ {lang_file} 存在")
            else:
                print(f"✗ {lang_file} 不存在")
    else:
        print("✗ 語言資源目錄不存在")


def main():
    """主函數 - 執行系統功能檢查"""
    print("="*50)
    print("電子交接系統功能實現檢查報告")
    print("="*50)
    
    check_backend_core_components()
    check_frontend_components()
    check_models_and_schemas()
    check_api_endpoints()
    check_spec_documents()
    check_language_resources()
    
    print("\n" + "="*50)
    print("檢查完成")
    print("如發現缺失文件，請重新運行相應的創建命令")
    print("="*50)


if __name__ == "__main__":
    main()