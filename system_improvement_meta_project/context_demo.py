#!/usr/bin/env python3
"""
Context Manager Demo - Real World Usage
======================================

Bu script Context Manager'ın gerçek kullanımını gösterir.
Session save, resume ve knowledge persistence işlemlerini test eder.
"""

from context_manager import ContextManager

def demo_context_management():
    """Context Management demo"""
    print("🧠 Context Manager - Real World Demo")
    print("=" * 60)
    
    # Real project context oluştur
    manager = ContextManager("YAPYOS_v2")
    
    # Current project state'ini analiz et ve session oluştur
    session_id = manager.create_session({
        "conversation_context": "Context Management System implementation",
        "current_focus": "Solving context limits and transaction interruptions",
        "user_need": "Seamless session continuity without knowledge loss"
    })
    
    print(f"\n🆔 Session Created: {session_id}")
    print(f"📁 Project: {manager.project_name}")
    
    # Current context summary
    summary = manager.generate_context_summary()
    print(f"\n📋 Current Context Summary:")
    print(summary)
    
    # Key knowledge points from this session
    knowledge_points = [
        "Context limits cause conversation interruptions requiring new sessions",
        "Context Manager provides persistent memory across sessions",
        "Session state includes tasks, files, conversation summary, knowledge points",
        "SQLite database stores persistent memory and knowledge graph",
        "Automated session resume eliminates repeated explanations",
        "Export functionality creates human-readable resume guides",
        "Autonomy Management System achieved 100% autonomous execution",
        "Risk-based permission framework enables safe autonomous operation",
        "Context management is the final critical piece for YAPYÖS v2.0"
    ]
    
    # Conversation summary
    conversation_summary = """
    Context Management System Implementation Session:
    
    1. User identified critical problem: context limits causing session interruptions
    2. Developed comprehensive Context Manager with SQLite persistence
    3. Implemented session state capture, save, and resume functionality
    4. Created knowledge base integration for cross-session memory
    5. Built export system for human-readable resume guides
    6. Tested with real project data - successfully captures current state
    7. Solution enables seamless long-term AI collaboration
    
    Key Achievement: Context continuity problem solved with intelligent persistence.
    """
    
    # Save session state
    print(f"\n💾 Saving session state...")
    success = manager.save_session_state(
        conversation_summary=conversation_summary,
        knowledge_points=knowledge_points
    )
    
    print(f"Session saved: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    # Generate and export resume guide
    print(f"\n📄 Generating resume guide...")
    resume_guide = manager.export_session_resume_guide()
    
    # Show sample of resume guide
    lines = resume_guide.split('\n')
    print("Resume Guide Preview:")
    for i, line in enumerate(lines[:25]):  # First 25 lines
        print(f"  {line}")
    if len(lines) > 25:
        print(f"  ... and {len(lines) - 25} more lines")
    
    # Test session resume
    print(f"\n🔄 Testing session resume...")
    resumed_session = manager.resume_session(session_id)
    
    if resumed_session:
        print(f"✅ Session resumed successfully!")
        print(f"  Session ID: {resumed_session.session_id}")
        print(f"  Timestamp: {resumed_session.timestamp}")
        print(f"  Knowledge Points: {len(resumed_session.knowledge_points)}")
        print(f"  Active Tasks: {len(resumed_session.current_tasks)}")
        print(f"  Completed Tasks: {len(resumed_session.completed_tasks)}")
    else:
        print(f"❌ Session resume failed")
    
    # Memory search test
    print(f"\n🔍 Testing memory search...")
    memories = manager.search_memory("autonomous", limit=5)
    print(f"Found {len(memories)} memories for 'autonomous':")
    for memory in memories:
        print(f"  • {memory.content[:80]}...")
    
    # Statistics
    stats = manager.get_session_statistics()
    print(f"\n📊 Context Manager Statistics:")
    for key, value in stats.items():
        if key != "current_session":
            print(f"  {key}: {value}")
    
    if "current_session" in stats:
        print(f"  Current Session Details:")
        for k, v in stats["current_session"].items():
            print(f"    {k}: {v}")
    
    # Usage instructions
    print(f"\n📖 How to Use This in Next Session:")
    print(f"   1. Start new conversation/session")
    print(f"   2. Run: python context_demo.py")
    print(f"   3. Or use manually:")
    print(f"      from context_manager import ContextManager")
    print(f"      manager = ContextManager('YAPYOS_v2')")
    print(f"      session = manager.resume_session()")
    print(f"      summary = manager.generate_context_summary()")
    print(f"      print(summary)")
    
    print(f"\n🎉 Context Management Demo Complete!")
    print(f"✅ Session persistence ready for cross-conversation continuity!")
    
    return manager, session_id

def quick_resume_demo():
    """Quick resume functionality demo"""
    print("\n" + "="*60)
    print("🚀 Quick Resume Demo")
    print("="*60)
    
    manager = ContextManager("YAPYOS_v2")
    
    # Try to resume latest session
    latest_session = manager.resume_session()
    
    if latest_session:
        print(f"✅ Resumed latest session: {latest_session.session_id}")
        
        # Generate fresh context summary
        summary = manager.generate_context_summary()
        print(f"\n📋 Context Summary:")
        print(summary)
        
        # Show recent knowledge
        if latest_session.knowledge_points:
            print(f"\n🧠 Recent Knowledge ({len(latest_session.knowledge_points)} points):")
            for i, point in enumerate(latest_session.knowledge_points[-5:], 1):  # Last 5
                print(f"  {i}. {point}")
        
        print(f"\n✅ You can now continue exactly where you left off!")
        
    else:
        print(f"❌ No previous session found to resume")
    
    return manager

if __name__ == "__main__":
    # Full demo
    manager, session_id = demo_context_management()
    
    # Quick resume test
    quick_resume_demo() 