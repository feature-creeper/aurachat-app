from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class Fan:
    """Model representing a fan in a chat."""
    id: int
    name: str
    username: str
    display_name: str
    about: str
    avatar: Optional[str]
    header: Optional[str]
    notice: str
    can_chat: bool
    can_earn: bool
    tips_max: int
    tips_min: int
    website: Optional[str]
    is_friend: bool
    join_date: str
    last_seen: Optional[str]
    location: Optional[str]
    wishlist: Optional[str]
    can_report: bool
    has_labels: bool
    has_stream: bool
    is_blocked: bool
    has_stories: bool
    header_size: Optional[str]
    is_verified: bool
    posts_count: int
    audios_count: int
    can_restrict: bool
    is_performer: bool

@dataclass
class Message:
    """Model representing a message in a chat."""
    response_type: str
    text: str
    giphy_id: Optional[str]
    locked_text: bool
    is_free: bool
    price: float
    is_media_ready: bool
    media_count: int
    media: List[Dict[str, Any]]
    previews: List[Dict[str, Any]]
    is_tip: bool
    is_reported_by_me: bool
    is_couple_people_media: bool
    queue_id: int
    is_markdown_disabled: bool
    release_forms: List[Dict[str, Any]]
    from_user: Dict[str, Any]
    is_from_queue: bool
    id: int
    is_opened: bool
    is_new: bool
    created_at: str
    changed_at: str
    cancel_seconds: int
    is_liked: bool
    can_purchase: bool
    can_purchase_reason: str
    can_report: bool
    can_be_pinned: bool
    is_pinned: bool

@dataclass
class Chat:
    """Model representing a chat in the system."""
    fan: Fan
    can_not_send_reason: bool
    can_send_message: bool
    can_go_to_profile: bool
    unread_messages_count: int
    has_unread_tips: bool
    is_muted_notifications: bool
    last_message: Message
    last_read_message_id: int
    has_purchased_feed: bool
    count_pinned_messages: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chat':
        """Create a Chat object from a dictionary."""
        if not data:
            raise ValueError("Empty chat data")
            
        # If fan data is at root level, use it directly
        fan_data = data if 'id' in data else data.get('fan', {}) or {}
        last_message_data = data.get('lastMessage', {}) or {}
        
        # Debug logging
        print("Raw fan data:", fan_data)
        
        # Create Fan object with default values
        fan = Fan(
            id=fan_data.get('id', 0),
            name=fan_data.get('name', ''),
            username=fan_data.get('username', ''),
            display_name=fan_data.get('displayName', ''),
            about=fan_data.get('about', ''),
            avatar=fan_data.get('avatar'),
            header=fan_data.get('header'),
            notice=fan_data.get('notice', ''),
            can_chat=fan_data.get('canChat', False),
            can_earn=fan_data.get('canEarn', False),
            tips_max=fan_data.get('tipsMax', 0),
            tips_min=fan_data.get('tipsMin', 0),
            website=fan_data.get('website'),
            is_friend=fan_data.get('isFriend', False),
            join_date=fan_data.get('joinDate', ''),
            last_seen=fan_data.get('lastSeen'),
            location=fan_data.get('location'),
            wishlist=fan_data.get('wishlist'),
            can_report=fan_data.get('canReport', False),
            has_labels=fan_data.get('hasLabels', False),
            has_stream=fan_data.get('hasStream', False),
            is_blocked=fan_data.get('isBlocked', False),
            has_stories=fan_data.get('hasStories', False),
            header_size=fan_data.get('headerSize'),
            is_verified=fan_data.get('isVerified', False),
            posts_count=fan_data.get('postsCount', 0),
            audios_count=fan_data.get('audiosCount', 0),
            can_restrict=fan_data.get('canRestrict', False),
            is_performer=fan_data.get('isPerformer', False)
        )
        
        # Create Message object with default values
        last_message = Message(
            response_type=last_message_data.get('responseType', ''),
            text=last_message_data.get('text', ''),
            giphy_id=last_message_data.get('giphyId'),
            locked_text=last_message_data.get('lockedText', False),
            is_free=last_message_data.get('isFree', False),
            price=last_message_data.get('price', 0.0),
            is_media_ready=last_message_data.get('isMediaReady', False),
            media_count=last_message_data.get('mediaCount', 0),
            media=last_message_data.get('media', []),
            previews=last_message_data.get('previews', []),
            is_tip=last_message_data.get('isTip', False),
            is_reported_by_me=last_message_data.get('isReportedByMe', False),
            is_couple_people_media=last_message_data.get('isCouplePeopleMedia', False),
            queue_id=last_message_data.get('queueId', 0),
            is_markdown_disabled=last_message_data.get('isMarkdownDisabled', False),
            release_forms=last_message_data.get('releaseForms', []),
            from_user=last_message_data.get('fromUser', {}),
            is_from_queue=last_message_data.get('isFromQueue', False),
            id=last_message_data.get('id', 0),
            is_opened=last_message_data.get('isOpened', False),
            is_new=last_message_data.get('isNew', False),
            created_at=last_message_data.get('createdAt', ''),
            changed_at=last_message_data.get('changedAt', ''),
            cancel_seconds=last_message_data.get('cancelSeconds', 0),
            is_liked=last_message_data.get('isLiked', False),
            can_purchase=last_message_data.get('canPurchase', False),
            can_purchase_reason=last_message_data.get('canPurchaseReason', ''),
            can_report=last_message_data.get('canReport', False),
            can_be_pinned=last_message_data.get('canBePinned', False),
            is_pinned=last_message_data.get('isPinned', False)
        )
        
        return cls(
            fan=fan,
            can_not_send_reason=data.get('canNotSendReason', False),
            can_send_message=data.get('canSendMessage', False),
            can_go_to_profile=data.get('canGoToProfile', False),
            unread_messages_count=data.get('unreadMessagesCount', 0),
            has_unread_tips=data.get('hasUnreadTips', False),
            is_muted_notifications=data.get('isMutedNotifications', False),
            last_message=last_message,
            last_read_message_id=data.get('lastReadMessageId', 0),
            has_purchased_feed=data.get('hasPurchasedFeed', False),
            count_pinned_messages=data.get('countPinnedMessages', 0)
        ) 