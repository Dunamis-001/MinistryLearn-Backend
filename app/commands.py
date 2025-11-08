"""
Flask CLI command to create example ministry courses
Run with: flask create-example-courses
"""

import click
from flask.cli import with_appcontext
from app.extensions import db
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.assessment import Assessment
from app.models.question import Question
from app.models.option import Option
from app.models.user import User
from datetime import datetime, timedelta
import json

@click.command('create-example-courses')
@with_appcontext
def create_example_courses():
    """Create 5 example ministry courses with modules and lessons"""
    
    # Find or create an admin user
    admin = User.query.filter_by(email='admin@ministrylearn.com').first()
    if not admin:
        click.echo("Please create an admin user first or update the script with an existing admin email")
        return
    
    # Check if admin has Admin role
    if not admin.has_role('Admin'):
        click.echo("User is not an admin. Please ensure the user has Admin role.")
        return
    
    courses_data = [
        {
            "title": "Introduction to Biblical Studies",
            "description": "A foundational course exploring the Bible's structure, themes, and interpretation methods. Perfect for new believers and those seeking to deepen their understanding of Scripture.",
            "category": "Bible Study",
            "difficulty": "Beginner",
            "campus": "Main Campus",
            "thumbnail_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=800",
            "modules": [
                {
                    "title": "Understanding the Bible",
                    "position": 1,
                    "lessons": [
                        {
                            "title": "What is the Bible?",
                            "content": """The Bible is a collection of 66 books written over thousands of years by various authors inspired by God. It's divided into the Old Testament (39 books) and New Testament (27 books). The Bible serves as God's revelation to humanity, containing history, poetry, prophecy, wisdom literature, and letters that guide our faith and practice.

## Understanding the Bible's Purpose

The Bible is not just a historical document or a collection of religious texts. It is God's living Word, designed to transform lives and reveal God's character and plan for humanity. Throughout its pages, we discover:

- **God's Character**: Who God is, His attributes, and His nature
- **Humanity's Condition**: Our need for salvation and relationship with God
- **God's Plan**: The story of redemption through Jesus Christ
- **Practical Guidance**: Wisdom for daily living and decision-making

## The Two Testaments

**Old Testament (39 books)**: Written primarily in Hebrew, the Old Testament covers:
- The creation of the world and humanity
- The history of Israel
- God's law and covenant with His people
- Prophecies about the coming Messiah
- Poetry and wisdom literature

**New Testament (27 books)**: Written in Greek, the New Testament includes:
- The four Gospels (Matthew, Mark, Luke, John) - accounts of Jesus' life
- The book of Acts - the early church's history
- Epistles (letters) to churches and individuals
- The book of Revelation - prophecy about the end times

## Why It Matters

The Bible is foundational to Christian faith because it:
1. Reveals God's truth and will
2. Provides guidance for life
3. Strengthens faith through stories of God's faithfulness
4. Transforms hearts and minds
5. Equips believers for service

As you study Scripture, remember that it's not just information to learn, but truth to live by. The Bible is meant to be read, understood, and applied to your daily life.""",
                            "position": 1,
                            "study_materials": [
                                {"type": "pdf", "title": "Bible Overview Guide", "url": "https://example.com/bible-overview.pdf"},
                                {"type": "link", "title": "Bible Reading Plan", "url": "https://example.com/reading-plan"},
                                {"type": "text", "title": "Key Bible Statistics", "content": "66 books total\n39 Old Testament books\n27 New Testament books\nWritten over ~1,500 years\n~40 different authors\nOriginally written in Hebrew, Aramaic, and Greek"}
                            ],
                            "assessment": {
                                "title": "What is the Bible? - Quiz",
                                "total_points": 100,
                                "questions": [
                                    {
                                        "prompt": "How many books are in the Bible?",
                                        "type": "mcq",
                                        "points": 20,
                                        "options": [
                                            {"text": "66 books", "is_correct": True},
                                            {"text": "39 books", "is_correct": False},
                                            {"text": "27 books", "is_correct": False},
                                            {"text": "73 books", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "The Old Testament contains how many books?",
                                        "type": "mcq",
                                        "points": 20,
                                        "options": [
                                            {"text": "27 books", "is_correct": False},
                                            {"text": "39 books", "is_correct": True},
                                            {"text": "66 books", "is_correct": False},
                                            {"text": "50 books", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "What are the four Gospels?",
                                        "type": "mcq",
                                        "points": 30,
                                        "options": [
                                            {"text": "Matthew, Mark, Luke, John", "is_correct": True},
                                            {"text": "Genesis, Exodus, Leviticus, Numbers", "is_correct": False},
                                            {"text": "Romans, Corinthians, Galatians, Ephesians", "is_correct": False},
                                            {"text": "Isaiah, Jeremiah, Ezekiel, Daniel", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "The Bible was written over approximately how many years?",
                                        "type": "mcq",
                                        "points": 15,
                                        "options": [
                                            {"text": "500 years", "is_correct": False},
                                            {"text": "1,000 years", "is_correct": False},
                                            {"text": "1,500 years", "is_correct": True},
                                            {"text": "2,000 years", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "What is the primary purpose of the Bible?",
                                        "type": "mcq",
                                        "points": 15,
                                        "options": [
                                            {"text": "To provide historical information", "is_correct": False},
                                            {"text": "To reveal God's character and plan for humanity", "is_correct": True},
                                            {"text": "To serve as a religious text", "is_correct": False},
                                            {"text": "To document ancient cultures", "is_correct": False}
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "title": "The Structure of Scripture",
                            "content": """Learn about the different genres in the Bible: historical books, poetry, prophecy, gospels, and epistles. Understanding these genres helps us interpret Scripture correctly. Each genre requires different reading approaches and understanding of context.

## Major Genres in the Bible

### Historical Books
The historical books (Genesis through Esther in the Old Testament, Acts in the New Testament) tell the story of God's interaction with humanity. These books:
- Record actual events and people
- Show God's faithfulness throughout history
- Demonstrate consequences of obedience and disobedience
- Examples: Genesis, Exodus, 1-2 Samuel, Acts

### Poetry and Wisdom Literature
Poetry books (Job, Psalms, Proverbs, Ecclesiastes, Song of Songs) express emotions, worship, and wisdom:
- Use figurative language and imagery
- Express deep emotions and spiritual truths
- Provide practical wisdom for daily living
- Examples: Psalms (prayers and songs), Proverbs (wisdom sayings)

### Prophecy
Prophetic books (Isaiah through Malachi in OT, Revelation in NT) contain:
- Messages from God to His people
- Warnings about judgment
- Promises of restoration and hope
- Foretelling of future events (especially about the Messiah)

### Gospels
The four Gospels (Matthew, Mark, Luke, John) are:
- Biographical accounts of Jesus' life, death, and resurrection
- Written from different perspectives for different audiences
- The foundation of Christian faith

### Epistles (Letters)
The epistles (Romans through Jude) are:
- Letters written to churches and individuals
- Practical instruction for Christian living
- Doctrinal teaching and correction
- Examples: Romans (theology), 1 Corinthians (church issues), Ephesians (Christian identity)

## Why Genre Matters

Understanding genre helps us:
1. **Interpret correctly**: Poetry uses different language than history
2. **Apply appropriately**: Prophecy requires different application than wisdom literature
3. **Appreciate fully**: Each genre communicates truth in its unique way
4. **Avoid misinterpretation**: Taking poetry literally or history figuratively leads to confusion

## Reading Tips by Genre

- **Historical**: Look for God's character and human responses
- **Poetry**: Appreciate the imagery and emotional expression
- **Prophecy**: Understand the historical context and future fulfillment
- **Gospels**: Focus on Jesus' teachings and actions
- **Epistles**: Apply practical instructions to your life

As you read Scripture, pay attention to the genre and adjust your reading approach accordingly.""",
                            "position": 2,
                            "study_materials": [
                                {"type": "text", "title": "Bible Genres Reference", "content": "Historical: Genesis-Esther\nPoetry: Job-Song of Songs\nProphecy: Isaiah-Malachi\nGospels: Matthew-John\nEpistles: Romans-Jude\nApocalyptic: Revelation"},
                                {"type": "link", "title": "Bible Genre Study Guide", "url": "https://example.com/genre-guide"}
                            ],
                            "assessment": {
                                "title": "Bible Structure Quiz",
                                "total_points": 100,
                                "questions": [
                                    {
                                        "prompt": "Which books are considered poetry/wisdom literature?",
                                        "type": "mcq",
                                        "points": 25,
                                        "options": [
                                            {"text": "Job, Psalms, Proverbs", "is_correct": True},
                                            {"text": "Genesis, Exodus, Leviticus", "is_correct": False},
                                            {"text": "Matthew, Mark, Luke", "is_correct": False},
                                            {"text": "Isaiah, Jeremiah, Ezekiel", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "How many Gospels are in the New Testament?",
                                        "type": "mcq",
                                        "points": 25,
                                        "options": [
                                            {"text": "Three", "is_correct": False},
                                            {"text": "Four", "is_correct": True},
                                            {"text": "Five", "is_correct": False},
                                            {"text": "Six", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "Why is understanding genre important when reading the Bible?",
                                        "type": "mcq",
                                        "points": 50,
                                        "options": [
                                            {"text": "It helps us interpret and apply Scripture correctly", "is_correct": True},
                                            {"text": "It's not really important", "is_correct": False},
                                            {"text": "It only matters for scholars", "is_correct": False},
                                            {"text": "It helps us memorize verses faster", "is_correct": False}
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "title": "The Canon of Scripture",
                            "content": "Explore how the 66 books of the Bible were selected and recognized as authoritative Scripture. Understand the criteria used by early church leaders to determine which books belonged in the canon.",
                            "position": 3,
                            "study_materials": [
                                {"type": "pdf", "title": "Canon Formation History", "url": "https://example.com/canon-history.pdf"}
                            ]
                        }
                    ]
                },
                {
                    "title": "Biblical Interpretation",
                    "position": 2,
                    "lessons": [
                        {
                            "title": "Hermeneutics: The Art of Interpretation",
                            "content": """Hermeneutics is the science and art of biblical interpretation. Learn key principles: context, genre, historical background, and the author's original intent. Proper interpretation requires understanding the original audience and cultural context.

## What is Hermeneutics?

Hermeneutics comes from the Greek word meaning "to interpret" or "to explain." In biblical studies, hermeneutics refers to the principles and methods used to understand and apply Scripture accurately. It's both a science (with rules and principles) and an art (requiring wisdom and discernment).

## Key Principles of Biblical Interpretation

### 1. Context is King
The most important principle: **never read a verse in isolation**. Consider:
- **Immediate context**: The verses before and after
- **Book context**: The overall message of the book
- **Biblical context**: How it fits with the rest of Scripture
- **Historical context**: The time and culture when it was written

### 2. Understand the Genre
Different genres require different approaches:
- **Narrative**: Look for the story's meaning and God's character
- **Poetry**: Appreciate imagery and emotional expression
- **Prophecy**: Consider historical context and future fulfillment
- **Epistles**: Apply practical instructions to your life

### 3. Consider Historical Background
Understanding the original audience helps us:
- Grasp the author's intended meaning
- See why certain instructions were given
- Apply timeless principles to modern situations

### 4. Look for the Author's Intent
Ask: "What did the original author intend to communicate to the original audience?" This prevents us from reading our own ideas into the text.

### 5. Let Scripture Interpret Scripture
The Bible is its own best interpreter. When unclear, look to:
- Other passages on the same topic
- Clear passages that explain difficult ones
- The overall teaching of Scripture

## Common Interpretation Mistakes

1. **Taking verses out of context**: "I can do all things" doesn't mean you can fly
2. **Ignoring genre**: Reading poetry literally or prophecy as history
3. **Applying everything directly**: Some instructions were for specific situations
4. **Reading our culture into the text**: Understanding ancient culture is crucial

## Practical Steps for Interpretation

1. **Read the passage multiple times** - First for understanding, then for details
2. **Ask questions**: Who? What? When? Where? Why? How?
3. **Look up difficult words** - Use a Bible dictionary or concordance
4. **Study the context** - Read surrounding chapters
5. **Check cross-references** - See how other passages relate
6. **Apply thoughtfully** - How does this apply to my life today?

## Application

Remember: Interpretation without application is incomplete. Once you understand what the text meant, ask:
- What does this mean for me today?
- How should this change my thinking or behavior?
- What timeless principles can I apply?

Good hermeneutics leads to accurate understanding, which leads to faithful application.""",
                            "position": 1,
                            "study_materials": [
                                {"type": "pdf", "title": "Interpretation Guide", "url": "https://example.com/interpretation.pdf"},
                                {"type": "text", "title": "Interpretation Checklist", "content": "✓ Read the passage multiple times\n✓ Check the immediate context\n✓ Consider the book's overall message\n✓ Understand the historical background\n✓ Identify the genre\n✓ Look for the author's intent\n✓ Check cross-references\n✓ Apply thoughtfully"}
                            ],
                            "assessment": {
                                "title": "Hermeneutics Quiz",
                                "total_points": 100,
                                "questions": [
                                    {
                                        "prompt": "What is the most important principle of biblical interpretation?",
                                        "type": "mcq",
                                        "points": 25,
                                        "options": [
                                            {"text": "Context is king", "is_correct": True},
                                            {"text": "Always read literally", "is_correct": False},
                                            {"text": "Trust your feelings", "is_correct": False},
                                            {"text": "Use modern translations only", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "Why is understanding genre important?",
                                        "type": "mcq",
                                        "points": 25,
                                        "options": [
                                            {"text": "Different genres require different reading approaches", "is_correct": True},
                                            {"text": "It's not really important", "is_correct": False},
                                            {"text": "It helps you memorize faster", "is_correct": False},
                                            {"text": "It makes the Bible easier to read", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "What should you consider when interpreting Scripture?",
                                        "type": "mcq",
                                        "points": 50,
                                        "options": [
                                            {"text": "Context, genre, historical background, and author's intent", "is_correct": True},
                                            {"text": "Only your personal opinion", "is_correct": False},
                                            {"text": "Modern culture only", "is_correct": False},
                                            {"text": "What sounds good to you", "is_correct": False}
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "title": "Applying Scripture Today",
                            "content": "Learn how to bridge the gap between ancient biblical texts and modern application. Discover principles for applying timeless truths to contemporary situations.",
                            "position": 2,
                            "study_materials": [
                                {"type": "text", "title": "Application Framework", "content": "1. Understand the original meaning\n2. Identify timeless principles\n3. Apply to modern context\n4. Consider cultural differences"}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Christian Leadership Fundamentals",
            "description": "Develop essential leadership skills grounded in biblical principles. Learn to lead with integrity, serve others, and build effective ministry teams.",
            "category": "Leadership",
            "difficulty": "Intermediate",
            "campus": "Main Campus",
            "thumbnail_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800",
            "modules": [
                {
                    "title": "Biblical Foundations of Leadership",
                    "position": 1,
                    "lessons": [
                        {
                            "title": "Servant Leadership Model",
                            "content": """Jesus modeled servant leadership when He washed His disciples' feet. True Christian leadership is about serving others, not being served. This lesson explores the radical nature of servant leadership in contrast to worldly leadership models.

## What is Servant Leadership?

Servant leadership is a leadership philosophy in which the leader's primary goal is to serve others. This concept was most clearly demonstrated by Jesus Christ, who said, "The Son of Man did not come to be served, but to serve" (Mark 10:45). When Jesus washed His disciples' feet, He was modeling a completely different approach to leadership than what the world teaches.

## The World's View vs. God's View

**Worldly Leadership:**
- Power and authority over others
- Being served by followers
- Climbing the ladder of success
- Using position for personal gain
- Commanding and controlling

**Servant Leadership:**
- Power and authority to serve others
- Serving followers sacrificially
- Empowering others to succeed
- Using position to benefit others
- Leading by example and influence

## Key Principles of Servant Leadership

### 1. Humility
Servant leaders recognize that their position is not about personal glory but about serving God and others. They don't think less of themselves, but think of themselves less.

### 2. Service First
The servant leader's first question is: "How can I help?" rather than "What can I get?" They prioritize the needs of others above their own comfort and convenience.

### 3. Empowerment
Servant leaders don't hoard power; they give it away. They invest in developing others, equipping them to succeed, and celebrating their achievements.

### 4. Sacrificial Love
True servant leadership requires sacrifice. It means putting others' needs before your own, even when it's inconvenient or costly.

## Biblical Examples

- **Jesus**: The ultimate servant leader who gave His life for others
- **Moses**: Led Israel while serving them faithfully for 40 years
- **Paul**: Served the churches he planted, working with his own hands
- **Timothy**: Served alongside Paul, learning to lead by serving

## Practical Application

1. **Look for opportunities to serve**: Don't wait to be asked; proactively look for ways to help
2. **Lead by example**: Show others what servant leadership looks like through your actions
3. **Empower others**: Give people opportunities to lead and grow
4. **Celebrate others' success**: Rejoice when those you lead succeed
5. **Stay humble**: Remember that leadership is a stewardship, not a right

Servant leadership is counter-cultural, but it's the model Jesus gave us. When we lead by serving, we reflect His character and make a lasting impact.""",
                            "position": 1,
                            "study_materials": [
                                {"type": "link", "title": "Servant Leadership Article", "url": "https://example.com/servant-leadership"},
                                {"type": "text", "title": "Servant Leadership Checklist", "content": "✓ Do I seek to serve or be served?\n✓ Am I empowering others or hoarding power?\n✓ Do I celebrate others' success?\n✓ Am I willing to do the tasks I ask others to do?\n✓ Do I put others' needs before my own?"}
                            ],
                            "assessment": {
                                "title": "Servant Leadership Quiz",
                                "total_points": 100,
                                "questions": [
                                    {
                                        "prompt": "What is the primary goal of a servant leader?",
                                        "type": "mcq",
                                        "points": 25,
                                        "options": [
                                            {"text": "To serve others", "is_correct": True},
                                            {"text": "To gain power", "is_correct": False},
                                            {"text": "To be served", "is_correct": False},
                                            {"text": "To control others", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "Who is the ultimate example of servant leadership?",
                                        "type": "mcq",
                                        "points": 25,
                                        "options": [
                                            {"text": "Jesus Christ", "is_correct": True},
                                            {"text": "Moses", "is_correct": False},
                                            {"text": "King David", "is_correct": False},
                                            {"text": "Paul", "is_correct": False}
                                        ]
                                    },
                                    {
                                        "prompt": "What is a key characteristic of servant leadership?",
                                        "type": "mcq",
                                        "points": 50,
                                        "options": [
                                            {"text": "Humility and service to others", "is_correct": True},
                                            {"text": "Power and control", "is_correct": False},
                                            {"text": "Personal gain", "is_correct": False},
                                            {"text": "Being served by followers", "is_correct": False}
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "title": "Leading with Character",
                            "content": """Character is the foundation of effective leadership. Explore qualities like integrity, humility, and wisdom that define godly leaders. Learn how to develop these character traits in your own life.

## Why Character Matters

Character is who you are when no one is watching. It's the foundation that determines whether your leadership will stand the test of time. Skills can be learned, but character must be developed through intentional choices and God's transforming work in your life.

## Essential Character Qualities for Christian Leaders

### 1. Integrity
Integrity means being honest, trustworthy, and consistent in your words and actions. People follow leaders they can trust. When you say you'll do something, do it. When you make a mistake, admit it. Integrity builds credibility and respect.

**Biblical Example**: Daniel's integrity was so consistent that his enemies could find no fault in him except his devotion to God (Daniel 6:4-5).

### 2. Humility
Humility is not thinking less of yourself, but thinking of yourself less. Humble leaders recognize their dependence on God and value others. They're teachable, admit mistakes, and give credit where it's due.

**Biblical Example**: Moses was described as the most humble man on earth (Numbers 12:3), yet he led millions of people.

### 3. Wisdom
Wisdom is the ability to apply knowledge and understanding to make good decisions. It comes from God and is developed through prayer, study of Scripture, and learning from experience.

**Biblical Example**: Solomon asked God for wisdom to lead His people, and God granted it (1 Kings 3:9-12).

### 4. Courage
Leadership requires courage to make difficult decisions, stand for what's right, and face opposition. Courage isn't the absence of fear, but acting despite fear because you trust God.

**Biblical Example**: Joshua was told repeatedly to "be strong and courageous" as he led Israel into the Promised Land (Joshua 1:6-9).

### 5. Compassion
Effective leaders care about people. They're not just focused on tasks and goals, but on the well-being of those they lead. Compassion moves leaders to serve and help others.

**Biblical Example**: Jesus was moved with compassion when He saw the crowds (Matthew 9:36).

## Developing Character

Character is developed through:

1. **Daily Choices**: Small decisions shape your character over time
2. **Accountability**: Having people who speak truth into your life
3. **Spiritual Disciplines**: Prayer, Bible study, and worship
4. **Learning from Failure**: Mistakes can teach valuable lessons
5. **God's Work**: The Holy Spirit transforms us as we yield to Him

## The Character Test

Ask yourself:
- Do I keep my word even when it's inconvenient?
- Am I honest in all my dealings?
- Do I treat everyone with respect?
- Am I willing to admit when I'm wrong?
- Do I care about people more than results?

## The Impact of Character

When leaders have strong character:
- People trust and follow them
- Organizations have integrity
- Decisions are made with wisdom
- Teams feel safe and valued
- God's purposes are advanced

Remember: Your character will determine your leadership legacy. Invest in developing godly character, and your leadership will have lasting impact.""",
                            "position": 2,
                            "study_materials": [
                                {"type": "pdf", "title": "Character Development Guide", "url": "https://example.com/character.pdf"},
                                {"type": "text", "title": "Character Assessment Questions", "content": "1. Am I honest in all my dealings?\n2. Do I keep my word?\n3. Am I humble and teachable?\n4. Do I show compassion to others?\n5. Do I have courage to do what's right?\n6. Am I growing in wisdom?\n7. Do I treat everyone with respect?\n8. Am I accountable to others?"}
                            ]
                        }
                    ]
                },
                {
                    "title": "Building Effective Teams",
                    "position": 2,
                    "lessons": [
                        {
                            "title": "Team Dynamics in Ministry",
                            "content": """Learn how to build, motivate, and maintain effective ministry teams. Understand different roles, communication strategies, and conflict resolution. Discover how to create unity while valuing diversity.

## The Importance of Teams in Ministry

No one can accomplish God's work alone. Jesus chose twelve disciples, not one. The early church worked in teams (Acts 13:1-3). Effective ministry requires effective teams where people work together toward a common goal.

## Building Effective Teams

### 1. Define Clear Roles
Every team member needs to know:
- What they're responsible for
- What authority they have
- How their role fits into the bigger picture
- Who they report to and work with

**Example**: In a worship team, the leader, musicians, vocalists, and tech crew all have distinct but complementary roles.

### 2. Establish Communication Channels
Good communication prevents misunderstandings and builds trust. Establish:
- Regular team meetings
- Clear communication protocols
- Open channels for feedback
- Transparent decision-making processes

### 3. Set Shared Goals
Teams need a common vision and clear objectives. When everyone understands and owns the goals, they work together more effectively.

### 4. Foster Trust and Respect
Trust is the foundation of effective teams. Build trust by:
- Keeping your word
- Being transparent
- Valuing each person's contribution
- Creating a safe environment for honest communication

### 5. Celebrate Successes Together
Recognize and celebrate achievements as a team. This builds morale and reinforces the value of working together.

### 6. Address Conflicts Promptly
Conflict is inevitable, but it doesn't have to be destructive. Address issues:
- Directly and respectfully
- Quickly, before they escalate
- With a focus on resolution, not blame
- Following biblical principles (Matthew 18:15-17)

## Understanding Team Roles

Different people bring different strengths:
- **Visionaries**: See the big picture and future possibilities
- **Implementers**: Turn vision into action
- **Relational**: Build connections and maintain harmony
- **Analytical**: Think through details and potential problems
- **Creative**: Generate new ideas and solutions

## Creating Unity While Valuing Diversity

Unity doesn't mean uniformity. Effective teams:
- Value different perspectives and gifts
- Create space for everyone to contribute
- Focus on common goals while celebrating differences
- Learn from each other's unique experiences

## Biblical Principles for Teams

1. **Love one another** (John 13:34-35)
2. **Bear one another's burdens** (Galatians 6:2)
3. **Submit to one another** (Ephesians 5:21)
4. **Encourage one another** (1 Thessalonians 5:11)
5. **Work together for God's glory** (1 Corinthians 10:31)

## Maintaining Team Health

Regular check-ins:
- How is the team functioning?
- Are there unresolved conflicts?
- Do people feel valued and heard?
- Are we achieving our goals?
- How can we improve?

Remember: Strong teams don't happen by accident. They require intentional investment, clear communication, and a commitment to working together for God's purposes.""",
                            "position": 1,
                            "study_materials": [
                                {"type": "text", "title": "Team Building Checklist", "content": "1. Define clear roles\n2. Establish communication channels\n3. Set shared goals\n4. Foster trust and respect\n5. Celebrate successes\n6. Address conflicts promptly\n7. Value diversity\n8. Regular team check-ins"},
                                {"type": "link", "title": "Team Dynamics Resources", "url": "https://example.com/team-dynamics"}
                            ]
                        },
                        {
                            "title": "Delegation and Empowerment",
                            "content": """Effective leaders know how to delegate tasks and empower others. Learn principles for identifying team members' strengths and assigning responsibilities that help them grow.

## Why Delegation Matters

Delegation is not just about getting things done; it's about developing people. When you delegate effectively, you:
- Free yourself to focus on what only you can do
- Develop others' skills and confidence
- Multiply your impact
- Build a stronger, more capable team
- Follow Jesus' model of training disciples

## The Delegation Process

### 1. Identify What to Delegate
Not everything should be delegated. Consider delegating:
- Tasks that others can do as well or better
- Routine responsibilities
- Projects that provide growth opportunities
- Tasks that match someone's interests and gifts

Keep for yourself:
- Vision and strategic planning
- Critical decisions only you can make
- Tasks requiring your specific expertise
- Confidential matters

### 2. Choose the Right Person
Match tasks to people based on:
- **Skills**: Do they have the ability?
- **Interest**: Are they motivated?
- **Capacity**: Do they have time?
- **Growth potential**: Will this help them develop?

### 3. Provide Clear Instructions
When delegating, be clear about:
- **What** needs to be done
- **Why** it matters
- **When** it's due
- **How** much authority they have
- **What** success looks like

### 4. Provide Resources and Support
Set people up for success by:
- Giving them what they need
- Being available for questions
- Checking in periodically
- Offering guidance without micromanaging

### 5. Trust and Let Go
Once you've delegated:
- Resist the urge to micromanage
- Trust people to do their best
- Allow them to make some mistakes
- Focus on results, not methods

## Empowerment Principles

Empowerment goes beyond delegation - it's about giving people:
- **Authority**: The power to make decisions
- **Responsibility**: Ownership of outcomes
- **Resources**: What they need to succeed
- **Support**: Encouragement and guidance
- **Recognition**: Credit for their contributions

## Identifying Strengths

To delegate effectively, you need to know your team:
- **Observe**: Watch how people work
- **Ask**: What are they passionate about?
- **Test**: Give small assignments to see strengths
- **Listen**: Pay attention to what they say they enjoy
- **Assess**: Use tools or conversations to identify gifts

## Common Delegation Mistakes

1. **Delegating without clear instructions**: Leads to confusion
2. **Micromanaging**: Undermines trust and growth
3. **Delegating only undesirable tasks**: Demotivates people
4. **Not providing support**: Sets people up to fail
5. **Taking back delegated tasks**: Shows lack of trust

## Biblical Examples

- **Moses**: Delegated to judges (Exodus 18:13-26)
- **Jesus**: Sent out the 72 disciples (Luke 10:1-12)
- **Paul**: Trained Timothy and others to lead churches
- **Jethro**: Advised Moses on delegation (Exodus 18)

## The Benefits of Effective Delegation

When done well, delegation:
- Develops future leaders
- Increases team capacity
- Frees leaders for strategic work
- Builds trust and ownership
- Multiplies ministry impact

Remember: Your goal isn't just to get things done, but to develop people who can do them. Effective delegation is an investment in people and the future of your ministry.""",
                            "position": 2,
                            "study_materials": [
                                {"type": "pdf", "title": "Delegation Guide", "url": "https://example.com/delegation.pdf"},
                                {"type": "text", "title": "Delegation Checklist", "content": "✓ Identify what to delegate\n✓ Choose the right person\n✓ Provide clear instructions\n✓ Give necessary resources\n✓ Set clear expectations\n✓ Check in appropriately\n✓ Trust and let go\n✓ Provide feedback\n✓ Give credit for success"}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Effective Evangelism",
            "description": "Learn practical methods for sharing the Gospel with confidence and compassion. Develop skills to engage in meaningful spiritual conversations.",
            "category": "Evangelism",
            "difficulty": "Beginner",
            "campus": "Online",
            "thumbnail_url": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=800",
            "modules": [
                {
                    "title": "The Gospel Message",
                    "position": 1,
                    "lessons": [
                        {
                            "title": "Understanding the Gospel",
                            "content": "The Gospel is the good news that Jesus Christ died for our sins, was buried, and rose again. Learn to articulate this message clearly and simply. Understand the core components: sin, salvation, and surrender.",
                            "position": 1,
                            "study_materials": [
                                {"type": "pdf", "title": "Gospel Presentation Guide", "url": "https://example.com/gospel.pdf"}
                            ]
                        },
                        {
                            "title": "Sharing Your Testimony",
                            "content": "Your personal testimony is a powerful tool. Learn how to craft and share your story of how Jesus changed your life in 2-3 minutes. Make it relatable, authentic, and focused on what God has done.",
                            "position": 2,
                            "study_materials": [
                                {"type": "text", "title": "Testimony Template", "content": "1. Life before Christ (brief)\n2. How you met Christ (the turning point)\n3. Life after Christ (the difference)\n4. Current relationship with God"}
                            ]
                        }
                    ]
                },
                {
                    "title": "Evangelism Methods",
                    "position": 2,
                    "lessons": [
                        {
                            "title": "Relational Evangelism",
                            "content": "Building genuine relationships opens doors for spiritual conversations. Learn to love people authentically and share Christ naturally. Discover how to listen well and ask good questions.",
                            "position": 1,
                            "study_materials": [
                                {"type": "link", "title": "Relational Evangelism Resources", "url": "https://example.com/relational-evangelism"}
                            ]
                        },
                        {
                            "title": "Overcoming Evangelism Fears",
                            "content": "Many Christians struggle with fear when sharing their faith. Learn practical strategies for overcoming anxiety and building confidence in evangelism.",
                            "position": 2,
                            "study_materials": [
                                {"type": "pdf", "title": "Overcoming Fear Guide", "url": "https://example.com/evangelism-fear.pdf"}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Worship Ministry Essentials",
            "description": "Explore the biblical foundations of worship and develop practical skills for leading worship services. Learn about music, technology, and creating an atmosphere of worship.",
            "category": "Worship",
            "difficulty": "Intermediate",
            "campus": "Main Campus",
            "thumbnail_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800",
            "modules": [
                {
                    "title": "Theology of Worship",
                    "position": 1,
                    "lessons": [
                        {
                            "title": "What is True Worship?",
                            "content": "Worship is more than music - it's a lifestyle of honoring God. Explore what the Bible says about worship in spirit and truth. Understand that worship encompasses all of life, not just Sunday mornings.",
                            "position": 1,
                            "study_materials": [
                                {"type": "pdf", "title": "Worship Theology Guide", "url": "https://example.com/worship-theology.pdf"}
                            ]
                        },
                        {
                            "title": "Biblical Examples of Worship",
                            "content": "Study worship throughout Scripture: from the tabernacle to the early church. Learn timeless principles for worship today. See how worship has evolved while maintaining core elements.",
                            "position": 2,
                            "study_materials": [
                                {"type": "text", "title": "Worship Scriptures", "content": "Psalm 95:6-7 - Come, let us bow down\nJohn 4:23-24 - Worship in spirit and truth\nRomans 12:1 - Living sacrifice\nHebrews 13:15 - Sacrifice of praise"}
                            ]
                        }
                    ]
                },
                {
                    "title": "Practical Worship Leading",
                    "position": 2,
                    "lessons": [
                        {
                            "title": "Song Selection and Flow",
                            "content": "Learn how to choose songs that connect with your congregation and create a meaningful worship experience. Understand song keys, transitions, and flow. Create sets that tell a story and lead people into God's presence.",
                            "position": 1,
                            "study_materials": [
                                {"type": "link", "title": "Song Planning Resources", "url": "https://example.com/song-planning"}
                            ]
                        },
                        {
                            "title": "Using Technology in Worship",
                            "content": "Modern worship often involves technology. Learn best practices for using sound systems, projection, and streaming to enhance worship without distracting from it.",
                            "position": 2,
                            "study_materials": [
                                {"type": "pdf", "title": "Worship Tech Guide", "url": "https://example.com/worship-tech.pdf"}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Discipleship and Spiritual Growth",
            "description": "Discover pathways to deeper spiritual maturity. Learn about spiritual disciplines, mentoring relationships, and growing in Christlikeness.",
            "category": "Discipleship",
            "difficulty": "Beginner",
            "campus": "South Campus",
            "thumbnail_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=800",
            "modules": [
                {
                    "title": "Spiritual Disciplines",
                    "position": 1,
                    "lessons": [
                        {
                            "title": "Prayer and Meditation",
                            "content": "Prayer is communication with God. Learn different types of prayer: adoration, confession, thanksgiving, and supplication. Develop a consistent prayer life that transforms your relationship with God.",
                            "position": 1,
                            "study_materials": [
                                {"type": "pdf", "title": "Prayer Guide", "url": "https://example.com/prayer-guide.pdf"},
                                {"type": "link", "title": "Prayer Journal Template", "url": "https://example.com/prayer-journal"}
                            ]
                        },
                        {
                            "title": "Bible Study Methods",
                            "content": "Learn effective methods for studying Scripture: observation, interpretation, and application. Develop skills to understand and apply God's Word. Explore different study approaches including inductive, topical, and character studies.",
                            "position": 2,
                            "study_materials": [
                                {"type": "text", "title": "Bible Study Template", "content": "1. Observation: What does it say?\n2. Interpretation: What does it mean?\n3. Application: How does it apply to me?\n4. Reflection: How will I respond?"}
                            ]
                        },
                        {
                            "title": "Fasting and Solitude",
                            "content": "Explore the spiritual disciplines of fasting and solitude. Learn how these practices can deepen your relationship with God and help you hear His voice more clearly.",
                            "position": 3,
                            "study_materials": [
                                {"type": "pdf", "title": "Fasting Guide", "url": "https://example.com/fasting-guide.pdf"}
                            ]
                        }
                    ]
                },
                {
                    "title": "Mentoring and Accountability",
                    "position": 2,
                    "lessons": [
                        {
                            "title": "The Power of Mentoring",
                            "content": "Mentoring relationships accelerate spiritual growth. Learn how to find a mentor, be a mentor, and create accountability partnerships. Discover the biblical model of discipleship.",
                            "position": 1,
                            "study_materials": [
                                {"type": "pdf", "title": "Mentoring Guide", "url": "https://example.com/mentoring.pdf"}
                            ]
                        },
                        {
                            "title": "Building Accountability",
                            "content": "Accountability helps us stay on track in our spiritual journey. Learn how to create safe spaces for honest sharing and mutual encouragement.",
                            "position": 2,
                            "study_materials": [
                                {"type": "text", "title": "Accountability Questions", "content": "1. How is your time with God?\n2. How are your relationships?\n3. Are there any areas of struggle?\n4. How can I pray for you?"}
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    
    created_count = 0
    
    for course_info in courses_data:
        # Extract modules
        modules_data = course_info.pop('modules')
        
        # Create course
        course = Course(
            title=course_info['title'],
            description=course_info['description'],
            category=course_info['category'],
            difficulty=course_info['difficulty'],
            campus=course_info['campus'],
            thumbnail_url=course_info.get('thumbnail_url'),
            published=True,
            approved=True,
            approved_by=admin.id,
            approved_at=datetime.utcnow(),
            created_by=admin.id
        )
        
        db.session.add(course)
        db.session.flush()  # Get the course ID
        
        click.echo(f"Created course: {course.title}")
        
        # Create modules
        for module_info in modules_data:
            lessons_data = module_info.pop('lessons')
            
            module = Module(
                course_id=course.id,
                title=module_info['title'],
                position=module_info['position']
            )
            
            db.session.add(module)
            db.session.flush()
            
            click.echo(f"  Created module: {module.title}")
            
            # Create lessons
            for lesson_info in lessons_data:
                study_materials_json = None
                if 'study_materials' in lesson_info and lesson_info['study_materials']:
                    study_materials_json = json.dumps(lesson_info['study_materials'])
                
                lesson = Lesson(
                    module_id=module.id,
                    title=lesson_info['title'],
                    content=lesson_info.get('content'),
                    video_url=lesson_info.get('video_url'),
                    study_materials=study_materials_json,
                    position=lesson_info['position']
                )
                
                db.session.add(lesson)
                db.session.flush()
                click.echo(f"    Created lesson: {lesson.title}")
                
                # Create assessment if specified
                if 'assessment' in lesson_info and lesson_info['assessment']:
                    assessment_data = lesson_info['assessment']
                    assessment = Assessment(
                        course_id=course.id,
                        title=assessment_data.get('title', f"{lesson.title} - Quiz"),
                        type='quiz',
                        total_points=assessment_data.get('total_points', 100)
                    )
                    db.session.add(assessment)
                    db.session.flush()
                    
                    # Link assessment to lesson
                    lesson.assessment_id = assessment.id
                    
                    # Create questions
                    for q_idx, question_data in enumerate(assessment_data.get('questions', []), 1):
                        question = Question(
                            assessment_id=assessment.id,
                            prompt=question_data['prompt'],
                            type=question_data.get('type', 'mcq'),
                            points=question_data.get('points', 10),
                            position=q_idx
                        )
                        db.session.add(question)
                        db.session.flush()
                        
                        # Create options for MCQ
                        if question_data.get('type') == 'mcq' and 'options' in question_data:
                            for opt_idx, option_data in enumerate(question_data['options'], 1):
                                option = Option(
                                    question_id=question.id,
                                    text=option_data['text'],
                                    is_correct=option_data.get('is_correct', False)
                                )
                                db.session.add(option)
                    
                    click.echo(f"      Created assessment: {assessment.title}")
        
        created_count += 1
    
    db.session.commit()
    click.echo(f"\n✓ Successfully created {created_count} courses with modules, lessons, and assessments!")


@click.command('fix-leadership-thumbnail')
@with_appcontext
def fix_leadership_thumbnail():
    """Fix missing thumbnail for 'Leadership in Ministry' course"""
    course = Course.query.filter_by(title='Leadership in Ministry').first()
    if not course:
        click.echo("Course 'Leadership in Ministry' not found")
        return
    
    # Use the same thumbnail as Christian Leadership Fundamentals
    course.thumbnail_url = "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800"
    db.session.commit()
    click.echo(f"✓ Updated thumbnail for '{course.title}'")


@click.command('remove-all-videos')
@with_appcontext
def remove_all_videos():
    """Remove all video URLs from existing lessons"""
    lessons_with_videos = Lesson.query.filter(Lesson.video_url.isnot(None)).filter(Lesson.video_url != '').all()
    
    click.echo(f"Found {len(lessons_with_videos)} lessons with videos")
    
    if len(lessons_with_videos) == 0:
        click.echo("No lessons with videos found. All lessons already have no videos.")
        return
    
    updated_count = 0
    for lesson in lessons_with_videos:
        click.echo(f"Removing video from: {lesson.title} (ID: {lesson.id}) - Video URL: {lesson.video_url}")
        lesson.video_url = None
        db.session.add(lesson)
        updated_count += 1
    
    db.session.commit()
    click.echo(f"\n✓ Successfully removed videos from {updated_count} lesson(s)!")

