#!/usr/bin/env python3
"""
Autonomy Manager Live Demo
=========================

Bu script Autonomy Manager'ın gerçek script execution'ını gösterir.
"""

from autonomy_manager import AutonomyManager
import os

def demo_autonomous_execution():
    """Autonomous execution demo"""
    print("🚀 Autonomy Manager Live Execution Demo")
    print("=" * 60)
    
    # Manager'ı initialize et
    manager = AutonomyManager()
    
    # Demo scripts
    demo_scripts = [
        {
            "name": "Monitoring Script",
            "script": "otomatik_gorev_kontrolu.py",
            "context": {
                "operation_type": "monitor",
                "working_directory": os.getcwd(),
                "user_present": True
            }
        },
        {
            "name": "Linting Tool",
            "script": "markdown_linter.py",
            "context": {
                "operation_type": "validate", 
                "working_directory": os.getcwd(),
                "user_present": True
            }
        },
        {
            "name": "Meta Project Guard",
            "script": "meta_project_guard.py",
            "context": {
                "operation_type": "check",
                "working_directory": os.getcwd(),
                "user_present": True
            }
        }
    ]
    
    print(f"\n🎯 Autonomy Level: {manager.config['autonomy_level']}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    # Execute each script
    for i, demo in enumerate(demo_scripts, 1):
        print(f"\n{'='*20} Demo {i}: {demo['name']} {'='*20}")
        
        # Assess and execute
        result = manager.assess_and_execute(demo['script'], demo['context'])
        
        print(f"📄 Script: {result['script_path']}")
        print(f"⚠️  Risk Level: {result['risk_level']}")
        print(f"🔐 Permission: {result['permission']}")
        print(f"⏱️  Execution Time: {result['execution_time']:.3f}s")
        
        if result['success']:
            print(f"✅ Status: SUCCESS")
            if result.get('output'):
                print(f"📤 Output Preview: {result['output'][:200]}...")
        else:
            print(f"❌ Status: FAILED")
            if result.get('error'):
                print(f"🚨 Error: {result['error']}")
        
        print(f"🆔 Execution ID: {result['execution_id']}")
    
    # Final autonomy stats
    print(f"\n📊 Final Autonomy Statistics:")
    stats = manager.get_autonomy_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show execution log
    print(f"\n📋 Execution Log Summary:")
    for i, execution in enumerate(manager.execution_log, 1):
        status = "✅" if execution['success'] else "❌"
        print(f"  {i}. {execution['script_path']} | {execution['permission']} | {status}")
    
    print(f"\n🎉 Autonomous Execution Demo Completed!")
    
    # Calculate autonomy rate
    total = len(manager.execution_log)
    autonomous = sum(1 for ex in manager.execution_log if ex['permission'] == 'allow')
    if total > 0:
        autonomy_rate = (autonomous / total) * 100
        print(f"🎯 Autonomy Rate: {autonomy_rate:.1f}% ({autonomous}/{total} scripts ran autonomously)")
    
    return manager

if __name__ == "__main__":
    manager = demo_autonomous_execution() 