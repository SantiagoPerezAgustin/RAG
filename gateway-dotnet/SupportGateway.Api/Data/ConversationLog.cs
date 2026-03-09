namespace SupportGateway.Api.Data
{
    public class ConversationLog
    {
        public int Id { get; set; }
        public string? UserId { get; set; }
        public string? Channel { get; set; }
        public string? Message { get; set; }
        public string? Response { get; set; }
        public string? Summary { get; set; }
        public DateTime At { get; set; }
    }
}
