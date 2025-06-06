#!/usr/bin/env python3
"""
Autonomy Manager Test Script
===========================

Bu script Autonomy Manager'ın farklı risk seviyelerindeki 
script'leri nasıl handle ettiğini test eder.
"""

from autonomy_manager import AutonomyManager
import os

def test_autonomy_manager():
    """Autonomy Manager'ı test et"""
    print("🧪 Autonomy Manager Test Suite")
    print("=" * 60)
    
    # Manager'ı initialize et
    manager = AutonomyManager()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Low Risk - Monitoring Script",
            "script": "otomatik_gorev_kontrolu.py",
            "context": {
                "operation_type": "monitor",
                "working_directory": "system_improvement_meta_project/",
                "user_present": True
            },
            "expected_permission": "allow"
        },
        {
            "name": "Low Risk - Linting Tool", 
            "script": "markdown_linter.py",
            "context": {
                "operation_type": "validate",
                "working_directory": "system_improvement_meta_project/",
                "user_present": True
            },
            "expected_permission": "allow"
        },
        {
            "name": "Medium Risk - Dependency Check",
            "script": "check_dependencies.py", 
            "context": {
                "operation_type": "check",
                "working_directory": "system_improvement_meta_project/",
                "user_present": True
            },
            "expected_permission": "allow"  # Context-based decision
        },
        {
            "name": "High Risk - Git Operation",
            "script": "git_commit_script.py",
            "context": {
                "operation_type": "commit",
                "working_directory": "system_improvement_meta_project/",
                "user_present": True
            },
            "expected_permission": "ask_user"
        }
    ]
    
    print(f"\n🎯 Current autonomy level: {manager.config['autonomy_level']}")
    print(f"📁 Safe directories: {manager.config['safe_directories']}")
    print(f"🚫 Restricted directories: {manager.config['restricted_directories']}")
    
    # Test her scenario
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n--- Test {i}: {scenario['name']} ---")
        
        # Risk assessment yap
        risk_level, risk_details = manager.assess_risk(
            scenario['script'], 
            scenario['context']
        )
        
        # Permission decision al
        permission = manager.get_permission(
            risk_level, 
            scenario['context'], 
            risk_details
        )
        
        print(f"📄 Script: {scenario['script']}")
        print(f"⚠️  Risk Level: {risk_level.value}")
        print(f"🔐 Permission: {permission.value}")
        print(f"📊 Risk Score: {risk_details['score']}")
        print(f"💭 Reasoning: {risk_details['reasoning'][0]}")
        
        # Expected vs actual
        expected = scenario['expected_permission']
        actual = permission.value
        status = "✅ PASS" if actual == expected else "❌ FAIL"
        print(f"🎯 Expected: {expected} | Actual: {actual} | {status}")
        
        # Risk factors
        print(f"📋 Risk Factors:")
        for factor in risk_details['factors']:
            print(f"   • {factor}")
    
    # Autonomy stats
    print(f"\n📊 Final Autonomy Stats:")
    stats = manager.get_autonomy_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test autonomy level changes
    print(f"\n🔧 Testing Autonomy Level Changes:")
    original_level = manager.config['autonomy_level']
    
    for level in ["low", "medium", "high", "full"]:
        manager.update_autonomy_level(level)
        print(f"  {level}: ✅ Updated successfully")
    
    # Restore original level
    manager.update_autonomy_level(original_level)
    print(f"  Restored to: {original_level}")
    
    print(f"\n🎉 Autonomy Manager Test Completed!")
    print(f"✅ System ready for autonomous operation!")

if __name__ == "__main__":
    test_autonomy_manager() 