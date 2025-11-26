"""
電子交接本系統完整性檢查
"""
import sys
import os
from pathlib import Path

# 添加根目錄到 Python 路徑
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))


def check_python_imports():
    """檢查 Python 模組導入是否正常"""
    print("檢查 Python 模組導入...")
    
    required_modules = [
        "fastapi",
        "uvicorn", 
        "sqlalchemy",
        "bcrypt",
        "PIL",
        "pydantic",
        "pydantic_settings"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} 導入成功")
        except ImportError as e:
            print(f"✗ {module} 導入失敗: {e}")
            missing_modules.append(module)
    
    print(f"導入檢查完成，缺失模組數: {len(missing_modules)}")
    return len(missing_modules) == 0


def test_database_connection():
    """測試數據庫連接"""
    print("\n測試數據庫連接...")
    try:
        from backend.core.config import settings
        from sqlalchemy import create_engine
        from sqlalchemy.exc import SQLAlchemyError
        
        # 創建引擎
        engine = create_engine(settings.DATABASE_URL, echo=False)
        
        # 測試連接
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ 數據庫連接測試成功")
            return True
    except Exception as e:
        print(f"✗ 數據庫連接測試失敗: {e}")
        return False


def test_language_manager():
    """測試語言管理器功能"""
    print("\n測試語言管理器功能...")
    try:
        from backend.core.language_manager import lang_manager
        
        # 測試語言切換
        current_lang = lang_manager.get_current_language()
        print(f"✓ 當前語言: {current_lang}")
        
        # 測試翻譯功能
        test_key = "common.title"
        translated = lang_manager.get_text(test_key, "Default Title")
        print(f"✓ 翻譯測試 ('{test_key}' → '{translated}')")
        
        return True
    except Exception as e:
        print(f"✗ 語言管理器測試失敗: {e}")
        return False


def test_models():
    """測試數據模型"""
    print("\n測試數據模型...")
    try:
        # 嘗試導入主要的模型
        from backend.models.all_models import User, DailyReport, AttendanceRecord, EquipmentLog, LotLog
        print("✓ 數據模型導入成功")
        return True
    except Exception as e:
        print(f"✗ 數據模型測試失敗: {e}")
        return False


def main():
    """主函數 - 執行系統完整性檢查"""
    print("=" * 50)
    print("電子交接本系統完整性檢查")
    print("=" * 50)
    
    # 檢查 Python 模組導入
    imports_ok = check_python_imports()
    
    # 測試數據庫連接
    db_ok = test_database_connection()
    
    # 測試語言管理器
    lang_ok = test_language_manager()
    
    # 測試數據模型
    models_ok = test_models()
    
    print("\n" + "=" * 50)
    print("檢查結果摘要:")
    print(f"Python 模組導入: {'✓ 通過' if imports_ok else '✗ 失敗'}")
    print(f"數據庫連接: {'✓ 通過' if db_ok else '✗ 失敗'}")
    print(f"語言管理器: {'✓ 通過' if lang_ok else '✗ 失敗'}")
    print(f"數據模型: {'✓ 通過' if models_ok else '✗ 失敗'}")
    
    overall_success = imports_ok and db_ok and lang_ok and models_ok
    print(f"\n整體狀態: {'✓ 系統準備就緒' if overall_success else '✗ 需要解決問題'}")
    print("=" * 50)
    
    if overall_success:
        print("\n系統已準備就緒，可以執行以下命令啟動應用程式:")
        print("  python run_app.py")
    else:
        print("\n發現問題，請先解決後再嘗試啟動應用程式")
    
    return overall_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)