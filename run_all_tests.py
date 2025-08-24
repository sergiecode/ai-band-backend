"""
Ejecutor Completo de Pruebas para AI Band Backend
Creado por Sergie Code

Ejecuta todas las suites de pruebas y proporciona validación comprensiva.
"""

import sys
import subprocess
from pathlib import Path


def run_test_suite(test_file, suite_name):
    """Ejecutar una suite de pruebas específica y devolver resultados."""
    print(f"\n{'='*20} {suite_name} {'='*20}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ Error ejecutando {suite_name}: {e}")
        return False


def validate_app_functionality():
    """Validar que la aplicación principal funciona."""
    print(f"\n{'='*20} VALIDACIÓN DE APLICACIÓN {'='*20}")
    
    try:
        # Probar aplicación principal
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("✅ La aplicación principal se ejecuta exitosamente")
            print("✅ Archivos MIDI generados exitosamente")
            return True
        else:
            print("❌ La aplicación principal falló")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    
    except Exception as e:
        print(f"❌ Error validando aplicación: {e}")
        return False


def check_output_files():
    """Verificar que los archivos de salida se crean."""
    print(f"\n{'='*20} VALIDACIÓN DE ARCHIVOS DE SALIDA {'='*20}")
    
    output_dir = Path(__file__).parent / "src" / "output"
    expected_files = ["bass_track.mid", "drum_track.mid"]
    
    all_files_exist = True
    
    for file_name in expected_files:
        file_path = output_dir / file_name
        if file_path.exists() and file_path.stat().st_size > 0:
            print(f"✅ [OK] {file_name} existe y tiene contenido ({file_path.stat().st_size} bytes)")
        else:
            print(f"❌ [FALLO] {file_name} faltante o vacío")
            all_files_exist = False
    
    if all_files_exist:
        print("✅ Todos los archivos de salida esperados están presentes y válidos")
    
    return all_files_exist


def main():
    """Ejecutar todas las pruebas y validaciones."""
    print("🎸 AI Band Backend - Suite Completa de Pruebas")
    print("Creado por Sergie Code")
    print("=" * 60)
    
    test_results = []
    
    # Suites de pruebas a ejecutar
    test_suites = [
        ("test_ai_band.py", "Pruebas Básicas"),
        ("test_advanced.py", "Pruebas Avanzadas"),
        ("test_integration.py", "Pruebas de Integración"),
    ]
    
    # Ejecutar todas las suites de pruebas
    for test_file, suite_name in test_suites:
        test_path = Path(__file__).parent / test_file
        if test_path.exists():
            success = run_test_suite(test_file, suite_name)
            test_results.append((suite_name, success))
        else:
            print(f"❌ Archivo de prueba {test_file} no encontrado")
            test_results.append((suite_name, False))
    
    # Validar funcionalidad de la aplicación
    app_success = validate_app_functionality()
    test_results.append(("Validación de Aplicación", app_success))
    
    # Verificar archivos de salida
    files_success = check_output_files()
    test_results.append(("Archivos de Salida", files_success))
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN FINAL DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ [PASÓ]" if success else "❌ [FALLÓ]"
        print(f"{test_name:<30} {status}")
        if success:
            passed += 1
    
    print("-" * 60)
    print(f"📈 Total: {passed}/{total} suites de pruebas pasaron")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("🚀 ¡El AI Band Backend está funcionando perfectamente!")
        print("✅ ¡Listo para uso en producción!")
        print("🔗 ¡Listo para integración con otros proyectos!")
        print("\n📋 Próximos pasos:")
        print("  - Usar el backend en tus proyectos de música IA")
        print("  - Integrar con ai-band-plugin para soporte VST/AU")
        print("  - Agregar más modelos de IA para generación mejorada")
        print("  - Crear características de procesamiento de audio en tiempo real")
        return True
    else:
        print(f"\n❌ {total - passed} suite(s) de pruebas fallaron")
        print("🔧 Por favor corrige los problemas antes de usar en producción")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error del ejecutor de pruebas: {e}")
        sys.exit(1)
