
namespace py app.{{ service_name }}.thf



service {{ service_cls_name }} {

	string ping(1: i32 seq_id, 2: string ball),

}
